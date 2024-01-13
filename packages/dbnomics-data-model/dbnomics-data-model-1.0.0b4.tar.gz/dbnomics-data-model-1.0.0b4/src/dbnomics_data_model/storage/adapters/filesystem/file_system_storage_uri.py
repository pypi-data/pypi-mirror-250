from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import timedelta
from enum import Enum
from pathlib import Path
from typing import Final, Self, TypeVar

from pysolr import Solr

from dbnomics_data_model.dbnomics_solr_client import DBnomicsSolrClient
from dbnomics_data_model.dbnomics_solr_client.constants import DEFAULT_SOLR_TIMEOUT
from dbnomics_data_model.model.url import Url
from dbnomics_data_model.storage.adapters.filesystem.storage_variant import StorageVariant
from dbnomics_data_model.storage.adapters.filesystem.variants.json_lines.offsets.repo import JsonLinesSeriesOffsetRepo
from dbnomics_data_model.storage.adapters.filesystem.variants.json_lines.offsets.solr_repo import (
    SolrJsonLinesSeriesOffsetRepo,
)
from dbnomics_data_model.storage.errors.storage_uri import StorageUriParamValueParseError
from dbnomics_data_model.storage.storage_uri import StorageUri, StorageUriScheme
from dbnomics_data_model.utils import get_enum_values, parse_bool

__all__ = ["FileSystemStorageUri"]


T = TypeVar("T")


DETECT_VARIANT_PARAM_VALUE: Final = "detect"


@dataclass(frozen=True, kw_only=True)
class FileSystemStorageUriParams:
    single_provider: bool = False
    solr_timeout: timedelta | None = None
    solr_base_url: Url | None = None
    variant: StorageVariant | None = None

    @property
    def series_offset_repo(self) -> JsonLinesSeriesOffsetRepo | None:
        solr_timeout = self.solr_timeout
        solr_base_url = self.solr_base_url

        if solr_base_url is None:
            return None

        timeout = (DEFAULT_SOLR_TIMEOUT if solr_timeout is None else solr_timeout).total_seconds()
        solr_client = Solr(solr_base_url, timeout=timeout)
        dbnomics_solr_client = DBnomicsSolrClient(solr_client=solr_client)
        return SolrJsonLinesSeriesOffsetRepo(dbnomics_solr_client=dbnomics_solr_client)


@dataclass(frozen=True, kw_only=True)
class FileSystemStorageUri(StorageUri):
    params: FileSystemStorageUriParams = field(default_factory=FileSystemStorageUriParams)
    scheme: StorageUriScheme = field(default=StorageUriScheme.FILESYSTEM, init=False)

    @classmethod
    def create(cls, *, params_data: dict[str, str], path: Path) -> Self:
        params = parse_file_system_storage_uri_params(params_data)
        return cls(params=params, path=path)


class FileSystemStorageUriParam(Enum):
    SINGLE_PROVIDER = "single_provider"
    SOLR_BASE_URL = "solr_base_url"
    SOLR_TIMEOUT = "solr_timeout"
    VARIANT = "variant"


def parse_file_system_storage_uri_param(
    *,
    default: T,
    params_data: dict[str, str],
    param_name: str,
    parse: Callable[[str], T],
    valid_values: list[str] | None = None,
) -> T:
    param_value_str = params_data.get(param_name)
    if param_value_str is None:
        return default
    try:
        return parse(param_value_str)
    except Exception as exc:
        raise StorageUriParamValueParseError(
            parse=parse, param_name=param_name, param_value_str=param_value_str, valid_values=valid_values
        ) from exc


def parse_file_system_storage_uri_params(params_data: dict[str, str]) -> FileSystemStorageUriParams:
    single_provider = parse_file_system_storage_uri_param(
        parse=parse_bool,
        default=False,
        param_name=FileSystemStorageUriParam.SINGLE_PROVIDER.value,
        params_data=params_data,
        valid_values=["0", "1"],
    )

    solr_timeout = parse_file_system_storage_uri_param(
        parse=lambda v: timedelta(seconds=int(v)),
        default=None,
        param_name=FileSystemStorageUriParam.SOLR_TIMEOUT.value,
        params_data=params_data,
    )

    solr_base_url = parse_file_system_storage_uri_param(
        parse=Url.parse,
        default=None,
        param_name=FileSystemStorageUriParam.SOLR_BASE_URL.value,
        params_data=params_data,
    )

    variant = parse_file_system_storage_uri_param(
        parse=lambda v: None if v == DETECT_VARIANT_PARAM_VALUE else StorageVariant(v),
        default=None,
        param_name=FileSystemStorageUriParam.VARIANT.value,
        params_data=params_data,
        valid_values=sorted([DETECT_VARIANT_PARAM_VALUE, *get_enum_values(StorageVariant)]),
    )

    return FileSystemStorageUriParams(
        single_provider=single_provider, solr_timeout=solr_timeout, solr_base_url=solr_base_url, variant=variant
    )
