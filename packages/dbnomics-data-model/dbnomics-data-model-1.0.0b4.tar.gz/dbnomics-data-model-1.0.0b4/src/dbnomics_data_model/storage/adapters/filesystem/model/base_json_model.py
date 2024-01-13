from typing import Self, cast

from dbnomics_data_model.json_utils.dumping import dump_as_json_data, toolbox_dumper
from dbnomics_data_model.json_utils.errors import JsonDumpError, JsonParseTypeError
from dbnomics_data_model.json_utils.parsing import parse_json_data_as
from dbnomics_data_model.json_utils.types import JsonObject
from dbnomics_data_model.storage.adapters.filesystem.errors.json_model import JsonModelDumpError, JsonModelParseError


class BaseJsonObjectModel:
    @classmethod
    def from_json_data(cls, data: JsonObject) -> Self:
        try:
            return parse_json_data_as(data, type_=cls)
        except JsonParseTypeError as exc:
            raise JsonModelParseError(data=data) from exc

    def to_json_data(self) -> JsonObject:
        try:
            data = dump_as_json_data(self, dumper=toolbox_dumper)
        except JsonDumpError as exc:
            raise JsonModelDumpError(obj=self) from exc
        return cast(JsonObject, data)
