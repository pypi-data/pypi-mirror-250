from typing import Annotated, Final, Optional

from click import BadParameter
from typer import Abort, Argument, Context, Option

from dbnomics_data_model.cli.console import console
from dbnomics_data_model.cli.constants import REVISION
from dbnomics_data_model.cli.error_chain import format_error_chain
from dbnomics_data_model.cli.storage_utils import open_storage
from dbnomics_data_model.errors import DataModelError
from dbnomics_data_model.model.identifiers.dataset_id import DatasetId
from dbnomics_data_model.model.identifiers.types import ProviderCode

__all__ = ["list_"]

PROVIDER_CODE_METAVAR: Final = "PROVIDER_CODE"


def list_(
    *,
    ctx: Context,
    code_only: Annotated[bool, Option(help="Only show the provider codes")] = False,
    provider_code_str: Annotated[
        str, Argument(help="List the datasets of this provider", metavar=PROVIDER_CODE_METAVAR)
    ],
    revision_id: Annotated[
        Optional[str], Option("--revision", envvar=REVISION, help="List datasets at this revision")
    ] = None,
    sort: Annotated[bool, Option(help="Sort datasets by code")] = True,
) -> None:
    try:
        provider_code = ProviderCode.parse(provider_code_str)
    except Exception as exc:
        raise BadParameter(str(exc), param_hint=PROVIDER_CODE_METAVAR) from exc

    root_ctx_params = ctx.find_root().params
    storage_uri_or_dir: str = root_ctx_params["storage_uri_or_dir"]

    storage = open_storage(storage_uri_or_dir)

    for dataset_code in storage.iter_dataset_codes(provider_code, revision_id=revision_id, sort=sort):
        if code_only:
            console.print(str(dataset_code))
            continue

        dataset_id = DatasetId(provider_code, dataset_code)

        try:
            dataset_metadata = storage.load_dataset_metadata(dataset_id, revision_id=revision_id)
        except DataModelError as exc:
            console.print(format_error_chain(exc))
            raise Abort from exc

        console.print(dataset_metadata)
