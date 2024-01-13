from typing import Any, cast

from jsonalias import Json
from typedload.datadumper import Dumper
from typedload.exceptions import TypedloadException

from dbnomics_data_model.json_utils.serializing import serialize_json
from dbnomics_data_model.json_utils.typedload_utils import create_toolbox_dumper

from .errors import JsonDumpError

__all__ = ["dump_as_json_bytes", "dump_as_json_data"]


default_dumper = Dumper()
toolbox_dumper = create_toolbox_dumper()


def dump_as_json_bytes(value: Any, *, dumper: Dumper | None = None) -> bytes:
    data = dump_as_json_data(value, dumper=dumper)
    return serialize_json(data)


def dump_as_json_data(value: Any, *, dumper: Dumper | None = None) -> Json:
    if dumper is None:
        dumper = default_dumper
    try:
        data = dumper.dump(value)
    except TypedloadException as exc:
        raise JsonDumpError(value=value) from exc
    return cast(Json, data)
