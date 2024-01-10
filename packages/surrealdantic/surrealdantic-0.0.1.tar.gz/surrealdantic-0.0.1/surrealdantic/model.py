import json
from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID, uuid4

import numpy as np
from pydantic import BaseModel, ConfigDict, computed_field


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

    This class inherits from the BaseModel class and provides additional functionality for serialization and deserialization using JSON.

    Attributes:
        Config (class): A nested class that holds configuration options for the Model.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True, extra="allow")

    @computed_field
    def id(self) -> str:
        """
        Generates a unique identifier for the object.

        Returns:
            str: The unique identifier.
        """
        return str(uuid4())

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
            super().dict(  # type: ignore
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
