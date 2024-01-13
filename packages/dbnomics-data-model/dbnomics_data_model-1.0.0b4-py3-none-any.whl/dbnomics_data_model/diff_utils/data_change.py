from dataclasses import dataclass
from typing import Any

from rich.console import Console, ConsoleOptions, RenderResult
from rich.table import Table

from dbnomics_data_model.cli.formatters.numbers import format_delta
from dbnomics_data_model.cli.renderables.render_utils import render_value
from dbnomics_data_model.diff_utils.types import ChangePath, ChangeType


@dataclass(frozen=True, kw_only=True)
class DataChange:
    change_path: ChangePath
    change_type: ChangeType
    new_value: Any
    old_value: Any

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        grid = Table.grid(padding=(0, 1))

        grid.add_row("change type:", self.change_type.value)
        grid.add_row("change path:", self.formatted_change_path)

        if self.change_type != ChangeType.ADD:
            grid.add_row("old value:", render_value(self.old_value))

        if self.change_type != ChangeType.DELETE:
            grid.add_row("new value:", render_value(self.new_value))

        if isinstance(self.old_value, float) and isinstance(self.new_value, float):
            grid.add_row("value delta:", format_delta(self.old_value, self.new_value), style="grey53")

        yield grid

    @property
    def formatted_change_path(self) -> str:
        if not self.change_path:
            return "__ROOT__"

        return ".".join(map(str, self.change_path))
