from collections.abc import Sequence
from dataclasses import dataclass, fields
from typing import TYPE_CHECKING, Generic, TypeVar

from rich.console import Console, ConsoleOptions, RenderResult
from rich.table import Table

from dbnomics_data_model.cli.renderables.render_utils import render_value

if TYPE_CHECKING:
    from _typeshed import DataclassInstance


D = TypeVar("D", bound="DataclassInstance")


@dataclass(frozen=True)
class DataclassTable(Generic[D]):
    items: Sequence[D]

    def __post_init__(self) -> None:
        if not self.items:
            msg = f"{type(self).__name__} can't render an empty sequence of items"
            raise ValueError(msg)

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        assert self.items

        column_names = self.column_names
        if column_names is None:
            column_names = self.field_names

        table = Table(*column_names)

        for item in self.items:
            table.add_row(*(render_value(getattr(item, column_name)) for column_name in column_names))

        yield table

    @property
    def column_names(self) -> Sequence[str] | None:
        return None

    @property
    def field_names(self) -> Sequence[str]:
        assert self.items
        first_item = self.items[0]
        return [field.name for field in fields(first_item)]
