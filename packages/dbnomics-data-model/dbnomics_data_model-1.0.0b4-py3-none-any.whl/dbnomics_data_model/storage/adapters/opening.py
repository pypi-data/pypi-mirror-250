from pathlib import Path
from typing import assert_never

import daiquiri

from dbnomics_data_model.storage.adapters.filesystem.file_system_storage_session import FileSystemStorageSession
from dbnomics_data_model.storage.adapters.filesystem.file_system_storage_uri import (
    FileSystemStorageUri,
    FileSystemStorageUriParams,
)
from dbnomics_data_model.storage.adapters.filesystem.single_provider_file_system_storage import (
    SingleProviderFileSystemStorage,
)
from dbnomics_data_model.storage.errors.storage_uri import StorageUriMissingScheme
from dbnomics_data_model.storage.storage import Storage
from dbnomics_data_model.storage.storage_session import StorageSession
from dbnomics_data_model.storage.storage_uri import StorageUri

__all__ = [
    "open_storage_from_dir",
    "open_storage_from_uri_or_dir",
    "open_storage_session_from_dir",
    "open_storage_session_from_uri_or_dir",
    "parse_storage_uri_or_dir",
]


logger = daiquiri.getLogger(__name__)


def open_storage_from_dir(storage_dir: Path, *, ensure_dir: bool = False) -> "SingleProviderFileSystemStorage":
    if ensure_dir:
        storage_dir.mkdir(exist_ok=True)
    return SingleProviderFileSystemStorage(storage_dir=storage_dir)


def open_storage_from_uri_or_dir(storage_uri_or_dir: StorageUri | Path, *, ensure_dir: bool = False) -> "Storage":
    if isinstance(storage_uri_or_dir, StorageUri):
        return Storage.from_uri(storage_uri_or_dir)

    if isinstance(storage_uri_or_dir, Path):
        return open_storage_from_dir(storage_uri_or_dir, ensure_dir=ensure_dir)

    assert_never(storage_uri_or_dir)


def open_storage_session_from_dir(
    storage_dir: Path, *, ensure_dir: bool = False, session_name: str | None = None
) -> "FileSystemStorageSession":
    logger.debug("Opening FileSystemStorageSession from directory %s", storage_dir)
    if ensure_dir:
        storage_dir.mkdir(exist_ok=True)
    uri = FileSystemStorageUri(params=FileSystemStorageUriParams(single_provider=True), path=storage_dir)
    return FileSystemStorageSession.from_uri(uri, session_name=session_name)


def open_storage_session_from_uri_or_dir(
    storage_uri_or_dir: StorageUri | Path, *, ensure_dir: bool = False, session_name: str | None = None
) -> "StorageSession":
    if isinstance(storage_uri_or_dir, StorageUri):
        return StorageSession.from_uri(storage_uri_or_dir, session_name=session_name)

    if isinstance(storage_uri_or_dir, Path):
        return open_storage_session_from_dir(storage_uri_or_dir, ensure_dir=ensure_dir, session_name=session_name)

    assert_never(storage_uri_or_dir)


def parse_storage_uri_or_dir(storage_uri_or_dir_str: str) -> StorageUri | Path:
    try:
        return StorageUri.parse(storage_uri_or_dir_str)
    except StorageUriMissingScheme as exc:
        logger.debug(
            "Could not parse %r as a storage URI, falling back to a directory: %s", storage_uri_or_dir_str, exc
        )
        try:
            storage_dir = Path(storage_uri_or_dir_str)
        except Exception as exc:
            msg = f"{storage_uri_or_dir_str!r} is not a valid storage URI or directory"
            raise ValueError(msg) from exc

        return storage_dir
