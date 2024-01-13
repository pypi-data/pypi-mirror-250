from dataclasses import KW_ONLY, dataclass

from rich.console import Console, ConsoleOptions, RenderResult
from rich.table import Table

from dbnomics_data_model.cli.renderables.render_utils import render_value
from dbnomics_data_model.model.series import Series


@dataclass(frozen=True)
class SeriesMetadataRecord:
    series: Series

    _: KW_ONLY
    stats: bool = False

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        grid = Table.grid(padding=(0, 1))

        grid.add_row("code", render_value(self.series.code), style="bold")
        grid.add_row("name", render_value(self.series.name))
        grid.add_row("description", render_value(self.series.description))
        grid.add_row("notes", render_value(self.series.notes))
        grid.add_row("doc_href", render_value(self.series.doc_href))
        grid.add_row("dimensions", render_value(self.series.dimensions))
        grid.add_row("attributes", render_value(self.series.attributes))
        grid.add_row("updated_at", render_value(self.series.updated_at))
        grid.add_row("next_release_at", render_value(self.series.next_release_at))

        if self.stats:
            period_domain = self.series.period_domain
            grid.add_row(
                "period_domain", render_value(period_domain if period_domain is not None else "no observation")
            )

            value_range = self.series.value_range
            grid.add_row(
                "value_range", render_value(value_range if value_range is not None else "no numeric observation")
            )

        yield grid
