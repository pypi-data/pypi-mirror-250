from typing import Annotated, Final, Optional

from click import BadParameter
from typer import Abort, Argument, Context, Option

from dbnomics_data_model.cli.console import console
from dbnomics_data_model.cli.constants import REVISION
from dbnomics_data_model.cli.error_chain import format_error_chain
from dbnomics_data_model.cli.renderables.observation_table import ObservationTable
from dbnomics_data_model.cli.renderables.series_metadata_record import SeriesMetadataRecord
from dbnomics_data_model.cli.storage_utils import open_storage
from dbnomics_data_model.errors import DataModelError
from dbnomics_data_model.model.identifiers.series_id import SeriesId

__all__ = ["show"]


SERIES_ID_METAVAR: Final = "SERIES_ID"


def show(
    *,
    ctx: Context,
    revision_id: Annotated[
        Optional[str], Option("--revision", envvar=REVISION, help="Show series at this revision")
    ] = None,
    series_id_str: Annotated[str, Argument(help="Show this series", metavar=SERIES_ID_METAVAR)],
    metadata: Annotated[bool, Option(help="Show series metadata")] = True,
    observations: Annotated[bool, Option(help="Show series observations")] = True,
    stats: Annotated[bool, Option(help="Show series statistics")] = True,
) -> None:
    try:
        series_id = SeriesId.parse(series_id_str)
    except Exception as exc:
        raise BadParameter(str(exc), param_hint=SERIES_ID_METAVAR) from exc

    root_ctx_params = ctx.find_root().params
    storage_uri_or_dir: str = root_ctx_params["storage_uri_or_dir"]

    storage = open_storage(storage_uri_or_dir)

    try:
        series = storage.load_series(
            series_id,
            revision_id=revision_id,
            with_observations=observations or stats,
        )
    except DataModelError as exc:
        console.print(format_error_chain(exc))
        raise Abort from exc

    if metadata:
        console.print(SeriesMetadataRecord(series, stats=stats))

    if observations:
        console.print(ObservationTable(series))
