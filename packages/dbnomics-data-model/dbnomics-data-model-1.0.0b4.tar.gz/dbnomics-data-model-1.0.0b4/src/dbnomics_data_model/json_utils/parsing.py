from typing import TypeVar, cast

import msgspec
from jsonalias import Json
from typedload.exceptions import TypedloadException

from dbnomics_data_model.json_utils.typedload_utils import create_toolbox_loader
from dbnomics_data_model.json_utils.types import JsonObject

from .errors import JsonBytesParseError, JsonParseTypeError

__all__ = ["loader", "parse_json_bytes", "parse_json_bytes_as_object", "parse_json_data_as"]


T = TypeVar("T")


loader = create_toolbox_loader()


def parse_json_bytes(value: bytes) -> Json:
    """Parse a JSON document inside text bytes."""
    try:
        return cast(Json, msgspec.json.decode(value))
    except msgspec.DecodeError as exc:
        raise JsonBytesParseError(value=value) from exc


def parse_json_bytes_as_array(value: bytes) -> list[Json]:
    """Parse a JSON array inside text bytes.

    Raise a JsonParseError if JSON data could not be parsed.
    """
    data = parse_json_bytes(value)
    if not isinstance(data, list):
        raise JsonParseTypeError(data=data, expected_type=list)
    return data


def parse_json_bytes_as_object(value: bytes) -> JsonObject:
    """Parse a JSON object inside text bytes.

    Raise a JsonParseError if JSON data could not be parsed.
    """
    data = parse_json_bytes(value)
    if not isinstance(data, dict):
        raise JsonParseTypeError(data=data, expected_type=dict)
    return data


def parse_json_data_as(data: Json, *, type_: type[T]) -> T:
    try:
        return loader.load(data, type_=type_)
    except TypedloadException as exc:
        raise JsonParseTypeError(data=data, expected_type=type_) from exc
