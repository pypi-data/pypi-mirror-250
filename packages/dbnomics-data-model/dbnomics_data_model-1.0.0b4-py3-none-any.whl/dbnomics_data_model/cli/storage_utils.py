from typer import Abort

from dbnomics_data_model.cli.console import console
from dbnomics_data_model.storage.adapters import open_storage_from_uri_or_dir
from dbnomics_data_model.storage.adapters.opening import parse_storage_uri_or_dir
from dbnomics_data_model.storage.storage import Storage


def open_storage(storage_uri_or_dir_str: str) -> Storage:
    storage_uri_or_dir = parse_storage_uri_or_dir(storage_uri_or_dir_str)

    try:
        return open_storage_from_uri_or_dir(storage_uri_or_dir, ensure_dir=True)
    except Exception as exc:
        console.print_exception()
        console.print(f"Could not open storage from {storage_uri_or_dir!r}")
        raise Abort from exc
