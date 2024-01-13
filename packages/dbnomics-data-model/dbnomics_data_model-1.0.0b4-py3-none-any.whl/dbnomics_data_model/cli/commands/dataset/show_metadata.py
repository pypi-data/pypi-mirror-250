from typing import Annotated, Final, Optional

from click import BadParameter
from typer import Abort, Argument, Context, Option

from dbnomics_data_model.cli.console import console
from dbnomics_data_model.cli.constants import REVISION
from dbnomics_data_model.cli.error_chain import format_error_chain
from dbnomics_data_model.cli.storage_utils import open_storage
from dbnomics_data_model.errors import DataModelError
from dbnomics_data_model.model.identifiers.dataset_id import DatasetId

__all__ = ["show_metadata"]


DATASET_ID_METAVAR: Final = "DATASET_ID"


def show_metadata(
    *,
    ctx: Context,
    dataset_id_str: Annotated[str, Argument(help="Show this dataset", metavar=DATASET_ID_METAVAR)],
    revision_id: Annotated[
        Optional[str], Option("--revision", envvar=REVISION, help="Show dataset at this revision")
    ] = None,
) -> None:
    try:
        dataset_id = DatasetId.parse(dataset_id_str)
    except Exception as exc:
        raise BadParameter(str(exc), param_hint=DATASET_ID_METAVAR) from exc

    root_ctx_params = ctx.find_root().params
    storage_uri_or_dir: str = root_ctx_params["storage_uri_or_dir"]

    storage = open_storage(storage_uri_or_dir)

    try:
        dataset_metadata = storage.load_dataset_metadata(dataset_id, revision_id=revision_id)
    except DataModelError as exc:
        console.print(format_error_chain(exc))
        raise Abort from exc

    console.print(dataset_metadata)
