from typer import Typer

from .list import list_
from .log import log
from .show import show

__all__ = ["series_app"]


series_app = Typer(name="series", no_args_is_help=True)
series_app.command(name="list")(list_)
series_app.command(name="log")(log)
series_app.command(name="show")(show)
