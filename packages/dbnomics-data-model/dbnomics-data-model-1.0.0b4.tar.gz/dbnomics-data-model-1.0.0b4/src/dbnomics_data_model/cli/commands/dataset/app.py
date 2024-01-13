from typer import Typer

from .list import list_
from .show_metadata import show_metadata

__all__ = ["dataset_app"]


dataset_app = Typer(name="dataset", no_args_is_help=True)
dataset_app.command(name="list")(list_)
dataset_app.command(name="show-metadata")(show_metadata)
