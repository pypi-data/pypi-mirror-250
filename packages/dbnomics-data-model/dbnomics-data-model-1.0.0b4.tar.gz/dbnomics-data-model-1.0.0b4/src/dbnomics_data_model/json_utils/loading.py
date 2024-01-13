from pathlib import Path

from jsonalias import Json

from dbnomics_data_model.json_utils.parsing import parse_json_bytes
from dbnomics_data_model.json_utils.types import JsonObject

from .errors import JsonParseTypeError

__all__ = ["load_json_file", "load_json_array_from_file", "load_json_object_from_file"]


def load_json_file(file: Path) -> Json:
    """Return data from a JSON file.

    Raise a FileNotFoundError if file was not found.
    Raise a JsonParseError if JSON data could not be parsed.
    """
    with file.open("rb") as fd:
        text = fd.read()
    return parse_json_bytes(text)


def load_json_array_from_file(file: Path) -> list[Json]:
    """Return data from a file containing a JSON array.

    Raise a JsonParseError if JSON data could not be parsed.
    """
    data = load_json_file(file)
    if not isinstance(data, list):
        raise JsonParseTypeError(data=data, expected_type=list)
    return data


def load_json_object_from_file(file: Path) -> JsonObject:
    """Return data from a file containing a JSON object.

    Raise a JsonParseError if JSON data could not be parsed.
    """
    data = load_json_file(file)
    if not isinstance(data, dict):
        raise JsonParseTypeError(data=data, expected_type=dict)
    return data
