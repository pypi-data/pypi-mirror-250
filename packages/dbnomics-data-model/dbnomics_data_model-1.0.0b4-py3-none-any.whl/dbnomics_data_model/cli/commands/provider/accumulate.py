from typer import Context

from dbnomics_data_model.cli.storage_utils import open_storage

from .app import provider_app

__all__ = ["accumulate"]


@provider_app.command(name="accumulate")
def accumulate(*, ctx: Context) -> None:
    root_ctx_params = ctx.find_root().params
    storage_uri_or_dir: str = root_ctx_params["storage_uri_or_dir"]

    storage = open_storage(storage_uri_or_dir)

    # TODO API design
    for _change in storage.iter_changes():
        ...
