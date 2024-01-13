from typing import Annotated, Final, Optional

from click import BadParameter
from rich.padding import Padding
from typer import Argument, Context, Option

from dbnomics_data_model.cli.console import console
from dbnomics_data_model.cli.constants import REVISION
from dbnomics_data_model.cli.storage_utils import open_storage
from dbnomics_data_model.model.identifiers.series_id import SeriesId

__all__ = ["log"]


SERIES_ID_METAVAR: Final = "SERIES_ID"


def log(
    *,
    ctx: Context,
    series_id_str: Annotated[str, Argument(help="Show the log of this series", metavar=SERIES_ID_METAVAR)],
    patch: Annotated[bool, Option("-p", "--patch", help="Show series patch")] = False,
    revision_id: Annotated[
        Optional[str], Option("--revision", envvar=REVISION, help="Make the log start from this revision")
    ] = None,
) -> None:
    try:
        series_id = SeriesId.parse(series_id_str)
    except Exception as exc:
        raise BadParameter(str(exc), param_hint=SERIES_ID_METAVAR) from exc

    root_ctx_params = ctx.find_root().params
    storage_uri_or_dir: str = root_ctx_params["storage_uri_or_dir"]

    storage = open_storage(storage_uri_or_dir)

    for revision, series_patch in storage.iter_series_changes(series_id, start_revision_id=revision_id):
        console.print(revision)

        if patch:
            console.print("Patch:")
            console.print(Padding.indent(series_patch, 4))
            console.print()
