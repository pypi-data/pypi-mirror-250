import json
import os
from datetime import datetime
from decimal import Decimal
from typing import Any, AsyncGenerator, Generic, Optional, Type, TypeVar
from uuid import UUID

import numpy as np
from pydantic import BaseModel, ConfigDict
from surrealdb import Surreal

from .utils import robust, setup_logging


class Encoder(json.JSONEncoder):
    """
    Custom JSON encoder that handles special data types.

    This encoder extends the `json.JSONEncoder` class and provides custom
    serialization for specific data types such as `datetime`, `Decimal`, `UUID`,
    `numpy.ndarray`, and `numpy.generic`. For other data types, it falls back
    to the default serialization provided by the base class.

    Usage:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    encoder = SurrealEncoder()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    json_data = encoder.encode(data)

    Attributes:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    None
    """

    def default(self, o: Any):
        if isinstance(o, datetime):
            return o.astimezone().isoformat()
        if isinstance(o, Decimal):
            return float(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        if isinstance(o, np.generic):
            return o.item()
        if isinstance(o, UUID):
            return str(o)
        else:
            return super().default(o)


class Decoder(json.JSONDecoder):
    """
    Custom JSON decoder that handles decoding of datetime strings.

    Args:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    *args: Variable length argument list.
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    **kwargs: Arbitrary keyword arguments.

    Attributes:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    object_hook: The object hook function used for decoding.

    Methods:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    _object_hook: Custom object hook function that converts datetime strings to datetime objects.

    """

    def __init__(self, *args: Any, **kwargs: Any):
        json.JSONDecoder.__init__(self, object_hook=self._object_hook, *args, **kwargs)

    def _object_hook(self, o: Any):
        """
        Custom object hook function that converts datetime strings to datetime objects.

        Args:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        o: The object to be decoded.

        Returns:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        The decoded object.

        """
        if isinstance(o, str):
            try:
                return datetime.fromisoformat(o)
            except ValueError:
                return o

        else:
            return o


class Model(BaseModel):
    """
    A class representing a database Model.

    This class extends the `pydantic.BaseModel` class and provides additional
    functionality for interacting with the database. It also provides custom
    serialization and deserialization using JSON.

    Custom configuration is provided through the `ConfigDict` object making the schema more flexible and allowing working with arbitrary data types.

    Bumped to pydantic v2

    """

    id: str
    model_config = ConfigDict(arbitrary_types_allowed=True, extra="allow")

    def dict(
        self,
        *,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = True,
        **dumps_kwargs: Any,
    ):
        return self.model_dump(
            mode="python",
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            **dumps_kwargs,
        )

    def json(
        self,
        *,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = True,
        **dumps_kwargs: Any,
    ):
        return json.dumps(
            super().model_dump(
                by_alias=by_alias,
                exclude_unset=exclude_unset,
                exclude_defaults=exclude_defaults,
                exclude_none=exclude_none,
                **dumps_kwargs,
            ),
            cls=Encoder,
        )

    def model_dump_json(
        self,
        *,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = True,
        **dumps_kwargs: Any,
    ):
        return json.dumps(
            self.model_dump(
                mode="python",
                by_alias=by_alias,
                exclude_unset=exclude_unset,
                exclude_defaults=exclude_defaults,
                exclude_none=exclude_none,
                **dumps_kwargs,
            ),
            cls=Encoder,
        )


S = TypeVar("S", bound=BaseModel)
M = TypeVar("M", bound=Model)
logger = setup_logging(__name__)


class Repository(Generic[M, S], Surreal):
    """
    Repository class for interacting with the database.

    Args:
                                                                    Generic (Model): The pydantic model associated with the database table.
                                                                    Generic (Schema): The pydantic model associated with the database table.

    Attributes:
                                                                    model (Type[Schema]): The pydantic model associated with the database table.


    Methods:
                                                                    create_: Create a new item in the database.
                                                                    read_: Read an item from the database.
                                                                    update_: Update an item in the database.
                                                                    delete_: Delete an item from the database.
    """

    def __init__(
        self,
        *,
        model: Type[S],
        url: str = os.getenv("DATABASE_URL", "ws://db:8000/rpc"),
        max_size: int = 2**22,
    ):
        self.model = model
        super().__init__(url=url, max_size=max_size)

    @property
    def table_name(self) -> str:
        return self.model.__name__

    @robust
    async def create_(self, data: M) -> list[S]:
        """
        Create a new item in the database.

        Args:
                                                                        data (I): The item to be created. As the datamodel contract describes, the id field is not required since it is autogenerated by the database.
                                                                                                                                                                                                          The type safety of the values is enforced by the pydantic model.
                                                                        db (Surreal): The database connection.

        Returns:
                                                                        list[S]: A list with the created item.
        """
        response = await self.create(thing=self.table_name, data=data.model_dump())
        return [self.model(**res) for res in response]

    @robust
    async def read_(
        self,
        *,
        id: Optional[str] = None,
        where: Optional[dict[str, Any]] = None,
    ) -> list[S]:
        """
        Read an item from the database.

        Args:
                                                                        db (Surreal): The database connection.
                                                                        id (Optional[str]): The id of the item to be read.
                                                                        where (Optional[dict[str, Any]]): The where clause of the item to be read as a dictionary with the keys as the field names and the values as the field values.
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          The type safety of the values is up to the user.

        Returns:
                                                                        list[S]: A list with the item(s) that match(es) the query. If no item matches the query, an empty list is returned.
        """
        if not id and not where:
            response = await self.select(thing=self.table_name)
        elif id:
            response = await self.select(thing=id)
        elif where:
            query = (
                f"SELECT * FROM {self.table_name} WHERE "
                + " AND ".join([f"{key} = '{value}'" for key, value in where.items()])
                + ";"
            )
            response = await self.query(query)
        else:
            logger.error("Invalid query parameters. id: %s, where: %s", id, where)
            return []
        return [self.model(**res) for res in response]

    @robust
    async def update_(self, id: str, data: S) -> list[S]:
        """
        Update an item in the database.

        Args:
                                                                        id (str): The id of the item to be updated.
                                                                        data (S): The full patch of the item to be updated, even including the fields that are not going to be updated.
                                                                        db (Surreal): The database connection.

        Returns:
                                                                        list[S]: A list with the updated item.
        """
        response = await self.update(id, data.dict())  # type: ignore #[TODO] Migrate to pydantic v2
        if len(response) > 1:
            logger.error("Weird response from the database: %s", response)
            return []
        return [self.model(**res) for res in response]

    @robust
    async def delete_(self, id: str) -> list[S]:
        """
        Delete an item from the database.

        Args:
                                                                        id (str): The id of the item to be deleted.
                                                                        db (Surreal): The database connection.

        Returns:
                                                                        list[S]: Empty list.
        """
        response = await self.delete(id)
        if len(response):
            logger.error("Failed to delete item %s", id)
            return [self.model(**res) for res in response]
        return []

    @classmethod
    async def __call__(
        cls,
        namespace: str,
        key: str,
    ) -> AsyncGenerator[Surreal, None]:
        """
        Retrieves a database connection from the Surreal database.

        Args:
                                        namespace (str): The namespace of the database.
                                        key (str): The key of the database.

        Yields:
                                        Surreal: A database connection object.

        """
        async with cls(
            url=os.getenv("DATABASE_URL", "ws://db:8000/rpc"),
            max_size=2**22,
            model=Type[S],  # type: ignore
        ) as db:
            if db.client_state.value == 2:
                await db.connect()
            await db.use(namespace, key)
            yield db
