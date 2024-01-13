from abc import ABC
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from urllib.parse import parse_qsl, urlparse

from dbnomics_data_model.storage.errors.storage_uri import (
    StorageUriMissingScheme,
    StorageUriPathParseError,
    StorageUriQueryParseError,
    StorageUriSchemeParseError,
    StorageUriUrlParseError,
    UnsupportedStorageUriScheme,
)
from dbnomics_data_model.utils import get_enum_values

__all__ = ["StorageUri"]


@dataclass(frozen=True, kw_only=True)
class StorageUri(ABC):
    path: Path
    scheme: "StorageUriScheme"

    @classmethod
    def parse(cls, uri: str) -> "StorageUri":
        uri_components = parse_uri_components(uri)
        if uri_components.scheme == StorageUriScheme.FILESYSTEM:
            from dbnomics_data_model.storage.adapters.filesystem.file_system_storage_uri import FileSystemStorageUri

            return FileSystemStorageUri.create(params_data=uri_components.params_data, path=uri_components.path)

        raise UnsupportedStorageUriScheme(scheme=uri_components.scheme)

    def __str__(self) -> str:
        path = "" if self.path is None else self.path
        return f"{self.scheme}:{path}"


@dataclass(frozen=True, kw_only=True)
class StorageUriComponents:
    params_data: dict[str, str]
    path: Path
    scheme: "StorageUriScheme"


class StorageUriScheme(Enum):
    FILESYSTEM = "filesystem"


def parse_uri_components(uri: str) -> StorageUriComponents:
    try:
        parsed = urlparse(uri)
    except Exception as exc:
        raise StorageUriUrlParseError(uri=uri) from exc

    scheme_str = parsed.scheme
    if not scheme_str:
        raise StorageUriMissingScheme(uri=uri)
    try:
        scheme = StorageUriScheme(scheme_str)
    except ValueError as exc:
        raise StorageUriSchemeParseError(
            scheme=scheme_str, uri=uri, valid_values=get_enum_values(StorageUriScheme)
        ) from exc

    try:
        path = Path(parsed.path)
    except Exception as exc:
        raise StorageUriPathParseError(uri=uri, path=parsed.path) from exc

    try:
        params_data = dict(parse_qsl(parsed.query, strict_parsing=True))
    except Exception as exc:
        raise StorageUriQueryParseError(uri=uri, query=parsed.query) from exc

    return StorageUriComponents(params_data=params_data, path=path, scheme=scheme)
