from collections.abc import Sequence
from dataclasses import dataclass

from more_itertools import intersperse
from rich.console import Console, ConsoleOptions, NewLine, RenderResult

from dbnomics_data_model.diff_utils.data_change import DataChange


@dataclass(frozen=True, kw_only=True)
class DataPatch:
    changes: Sequence[DataChange]

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        if not self.changes:
            yield "No change"
            return

        yield from intersperse(NewLine(), self.changes)
