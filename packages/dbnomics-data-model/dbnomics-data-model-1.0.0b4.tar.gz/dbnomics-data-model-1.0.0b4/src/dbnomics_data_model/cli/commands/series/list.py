from typing import Annotated, Final, Optional

from click import BadParameter, UsageError
from typer import Argument, Context, Option

from dbnomics_data_model.cli.console import console
from dbnomics_data_model.cli.constants import REVISION
from dbnomics_data_model.cli.renderables.series_metadata_record import SeriesMetadataRecord
from dbnomics_data_model.cli.storage_utils import open_storage
from dbnomics_data_model.model.identifiers.dataset_id import DatasetId

__all__ = ["list_"]


DATASET_ID_METAVAR: Final = "DATASET_ID"


def list_(
    *,
    ctx: Context,
    dataset_id_str: Annotated[str, Argument(help="List the series of this dataset", metavar=DATASET_ID_METAVAR)],
    code_only: Annotated[bool, Option(help="Only show the provider codes")] = False,
    observations: Annotated[bool, Option(help="Show series observations")] = False,
    revision_id: Annotated[
        Optional[str], Option("--revision", envvar=REVISION, help="List series at this revision")
    ] = None,
    sort: Annotated[bool, Option(help="Sort series by code")] = True,
    stats: Annotated[bool, Option(help="Show series statistics")] = True,
) -> None:
    try:
        dataset_id = DatasetId.parse(dataset_id_str)
    except Exception as exc:
        raise BadParameter(str(exc), param_hint=DATASET_ID_METAVAR) from exc

    if code_only and stats:
        msg = "--stats can't be used with --code-only"
        raise UsageError(msg)

    root_ctx_params = ctx.find_root().params
    storage_uri_or_dir: str = root_ctx_params["storage_uri_or_dir"]

    storage = open_storage(storage_uri_or_dir)

    series_items = storage.iter_series(
        dataset_id,
        revision_id=revision_id,
        sort_by_code=sort,
        with_observations=observations or stats,
    )

    if code_only:
        assert not stats

        for series in series_items:
            console.print(series.code)

        return

    for series in series_items:
        console.print(SeriesMetadataRecord(series, stats=stats))
        console.print()
