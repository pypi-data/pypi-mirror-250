from typing import Annotated

from typer import Context, Option

from dbnomics_data_model.cli.console import console
from dbnomics_data_model.cli.renderables.provider_metadata_table import ProviderMetadataTable
from dbnomics_data_model.cli.storage_utils import open_storage

__all__ = ["list_"]


def list_(
    *,
    ctx: Context,
    code_only: Annotated[bool, Option(help="Only show the provider codes")] = False,
    sort: Annotated[bool, Option(help="Sort providers by code")] = True,
) -> None:
    root_ctx_params = ctx.find_root().params
    storage_uri_or_dir: str = root_ctx_params["storage_uri_or_dir"]

    storage = open_storage(storage_uri_or_dir)

    provider_codes = list(storage.iter_provider_codes(sort=sort))

    if code_only:
        for provider_code in provider_codes:
            console.print(provider_code)

        return

    provider_metadata_items = [storage.load_provider_metadata(provider_code) for provider_code in provider_codes]
    provider_metadata_table = ProviderMetadataTable(provider_metadata_items)
    console.print(provider_metadata_table)
