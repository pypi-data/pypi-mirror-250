from dataclasses import dataclass

from rich.console import Console, ConsoleOptions, RenderResult
from rich.table import Table

from dbnomics_data_model.model.constants import PERIOD, VALUE
from dbnomics_data_model.model.series import Series


@dataclass(frozen=True)
class ObservationTable:
    series: Series

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        series = self.series

        attribute_codes = sorted(series.get_observation_attribute_codes())
        column_names = [PERIOD, VALUE, *attribute_codes]

        table = Table(*column_names)

        for observation in series.observations:
            table.add_row(
                str(observation.period),
                observation.formatted_value,
                *(observation.attributes.get(attribute_code, "-") for attribute_code in attribute_codes),
            )

        yield table
