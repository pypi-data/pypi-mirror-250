from typing import Any

from rich.console import RenderableType


def render_value(value: Any) -> RenderableType:
    return value if hasattr(value, "__rich__") or hasattr(value, "__rich_console__") else str(value)
