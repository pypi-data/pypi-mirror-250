from typer import Typer

from .list import list_
from .show_metadata import show_metadata

__all__ = ["provider_app"]


provider_app = Typer(name="provider", no_args_is_help=True)
provider_app.command(name="list")(list_)
provider_app.command(name="show-metadata")(show_metadata)
