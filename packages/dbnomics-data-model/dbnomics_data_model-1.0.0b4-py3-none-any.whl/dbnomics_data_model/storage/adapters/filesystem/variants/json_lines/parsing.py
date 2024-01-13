import msgspec
from msgspec import Struct


class LineWithCode(Struct):
    code: str


def parse_json_line_code(line: bytes) -> str:
    line_with_code = msgspec.json.decode(line, type=LineWithCode)
    return line_with_code.code
