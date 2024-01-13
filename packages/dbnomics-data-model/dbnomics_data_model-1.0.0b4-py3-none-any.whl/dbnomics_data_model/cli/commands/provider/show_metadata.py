from typing import Annotated, Final, Optional

from click import BadParameter
from typer import Argument, Context, Option

from dbnomics_data_model.cli.console import console
from dbnomics_data_model.cli.constants import REVISION
from dbnomics_data_model.cli.storage_utils import open_storage
from dbnomics_data_model.model.identifiers.types import ProviderCode

__all__ = ["show_metadata"]


PROVIDER_CODE_METAVAR: Final = "PROVIDER_CODE"


def show_metadata(
    *,
    ctx: Context,
    provider_code_str: Annotated[str, Argument(help="Show this provider", metavar=PROVIDER_CODE_METAVAR)],
    revision_id: Annotated[
        Optional[str], Option("--revision", envvar=REVISION, help="Show provider at this revision")
    ] = None,
) -> None:
    try:
        provider_code = ProviderCode.parse(provider_code_str)
    except Exception as exc:
        raise BadParameter(str(exc), param_hint=PROVIDER_CODE_METAVAR) from exc

    root_ctx_params = ctx.find_root().params
    storage_uri_or_dir: str = root_ctx_params["storage_uri_or_dir"]

    storage = open_storage(storage_uri_or_dir)

    provider_metadata = storage.load_provider_metadata(provider_code, revision_id=revision_id)
    console.print(provider_metadata)
