import os
from typing import Any, AsyncGenerator, Generic, Optional, Type, TypeVar

from fastapi import APIRouter, Body, Depends, FastAPI, Query, Request
from sse_starlette.sse import EventSourceResponse

from .repository import BaseModel, Repository, Surreal
from .utils import robust

Model = TypeVar("Model", bound=BaseModel)
Schema = TypeVar("Schema", bound=BaseModel)


async def get_db(namespace: str, key: str) -> AsyncGenerator[Surreal, None]:
    """
    Retrieves a database connection from the Surreal database.

    Args:
        namespace (str): The namespace of the database.
        key (str): The key of the database.

    Yields:
        Surreal: A database connection object.

    """
    async with Surreal(
        url=os.getenv("DATABASE_URL", "ws://db:8000/rpc"), max_size=2**22
    ) as db:
        if db.client_state.value == 2:
            await db.connect()
        await db.use(namespace, key)
        yield db


def _get_query_params(request: Request) -> dict[str, Any]:
    return {
        key: value
        for key, value in request.query_params.items()
        if key not in ["namespace", "key", "id"]
    }


class Controller(APIRouter, Generic[Model, Schema]):
    """
    A generic controller class that can be used to create a REST API for a given model and schema.

    Args:
        APIRouter (APIRouter): The APIRouter class to inherit from.
        Generic (Generic[Model, Schema]): The generic types for the model and schema.
    """

    model: Type[Model]

    @property
    def repository(self) -> Repository[Schema, Model]:
        """
        Returns the repository associated with the controller.

        Returns:
            Repository[Schema, Model]: The repository object.
        """
        return Repository[Schema, Model](model=self.model)

    @robust
    async def post_(self, *, data: Schema, db: Surreal) -> list[Model]:
        """
        Create a new record in the database.

        Args:
            data (Schema): The data to be inserted.
            db (Surreal): The database connection.

        Returns:
            list[Model]: The list of created models.
        """
        return await self.repository.create_(data, db)

    @robust
    async def get_(
        self,
        *,
        db: Surreal,
        id: Optional[str] = None,
        where: Optional[dict[str, Any]] = None,
    ) -> list[Model]:
        """
        Retrieves records from the database based on the provided query parameters.

        Args:
            db (Surreal): The database connection object.
            id (Optional[str]): The ID of the record to retrieve. Defaults to None.
            where (Optional[dict[str, Any]]): The query parameters as a dictionary. Defaults to None.

        Returns:
            list[Model]: A list of Model objects representing the retrieved records.

        Raises:
            ValueError: If the query parameters are invalid.
        """
        if id is None and where is None:
            response = await db.select(self.model.__name__)
        elif id is not None:
            response = await db.select(id)
        elif where is not None:
            self._validate_select_query(where)
            query = (
                f"SELECT * FROM {self.model.__name__} WHERE "
                + " AND ".join([f"{key} = '{value}'" for key, value in where.items()])
                + ";"
            )
            response = await db.query(query)
        else:
            raise ValueError("Invalid query parameters.")
        return [self.model(**res) for res in response]

    @robust
    async def put_(self, *, id: str, data: Model, db: Surreal) -> list[Model]:
        """
        Update a model with the given ID in the database.

        Args:
            id (str): The ID of the model to update.
            data (Model): The updated data for the model.
            db (Surreal): The database connection.

        Returns:
            list[Model]: The updated model.
        """
        return await self.repository.update_(id, data, db)

    @robust
    async def delete_(self, *, id: str, db: Surreal) -> list[Model]:
        """
        Delete a model with the specified ID from the database.

        Args:
            id (str): The ID of the model to delete.
            db (Surreal): The database instance.

        Returns:
            list[Model]: The list of deleted models.
        """
        return await self.repository.delete_(id, db)

    def _validate_select_query(self, query: dict[str, Any]) -> None:
        for key, value in query.items():
            if not hasattr(self.model, key):
                raise ValueError(f"Invalid query parameter: {key}.")
            if not isinstance(value, type(getattr(self.model, key))):
                raise ValueError(
                    f"Invalid query parameter type: {type(value)} for {key}."
                )


def create_controller(
    *, body: Type[Schema], model: Type[Model]
) -> Controller[Model, Schema]:
    """
    Creates a controller instance for a given model and schema.

    Args:
        body (Type[Schema]): The schema class used for request validation.
        model (Type[Model]): The model class representing the database table.

    Returns:
        Controller[Model, Schema]: The created controller instance.
    """
    app = Controller[Model, Schema](
        prefix="/" + model.__name__.lower(), tags=[model.__name__]
    )
    app.model = model

    @app.get("/{namespace}/{key}")
    async def _(
        *,
        db: Surreal = Depends(get_db),
        id: Optional[str] = None,
        where: Optional[dict[str, Any]] = Depends(_get_query_params),
    ):
        return await app.get_(db=db, id=id, where=where if where else None)

    @app.post("/{namespace}/{key}")
    async def _(*, data: body = Body(...), db: Surreal = Depends(get_db)):
        return await app.post_(db=db, data=data)

    @app.put("/{namespace}/{key}")
    async def _(
        *,
        data: model = Body(...),
        db: Surreal = Depends(get_db),
        id: str = Query(...),
    ):
        return await app.put_(db=db, id=id, data=data)

    @app.delete("/{namespace}/{key}")
    async def _(*, db: Surreal = Depends(get_db), id: str = Query(...)):
        return await app.delete_(db=db, id=id)

    @app.get("/{namespace}/{key}/snapshot")
    async def _(*, namespace: str, key: str):
        async def generator():
            async with Surreal(
                url=os.getenv("DATABASE_URL", "ws://db:8000/rpc"),
                max_size=2**22,
            ) as db:
                if db.client_state.value == 2:
                    await db.connect()
                await db.use(namespace, key)
                table_name = app.repository.table_name
                query = f"SELECT * FROM {table_name};"
                snapshot = await db.query(query)
                for row in snapshot:
                    yield app.model(**row).model_dump()

        return EventSourceResponse(generator())

    return app


class AutoAPI(FastAPI):
    """
    Automatic Creation of REST APIs by registering models and schemas.
    """

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(title="AutoAPI", version="0.0.1", *args, **kwargs)

    def add(self, *, model: Type[Model], schema: Type[Schema]):
        """
        Adds a model and schema to the API.
        Automatically creates a controller for the model and schema.

        Args:
            model (Type[Model]): The model class representing the database table.
            schema (Type[Schema]): The schema class used for request validation.

        Returns:
            AutoAPI: The AutoAPI instance.
        """
        controller = create_controller(body=schema, model=model)
        self.include_router(controller)
        return self
