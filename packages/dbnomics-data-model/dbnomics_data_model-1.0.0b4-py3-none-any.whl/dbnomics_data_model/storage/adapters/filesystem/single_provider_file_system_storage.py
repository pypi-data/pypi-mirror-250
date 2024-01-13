from collections.abc import Iterator
from pathlib import Path

from dbnomics_data_model.model import ProviderCode
from dbnomics_data_model.storage.adapters.filesystem.file_system_storage import FileSystemStorage

__all__ = ["SingleProviderFileSystemStorage"]


class SingleProviderFileSystemStorage(FileSystemStorage):
    def delete_provider_dir(self, provider_code: ProviderCode, *, missing_ok: bool = False) -> None:  # noqa: ARG002
        msg = "delete_provider_dir is a forbidden method with SingleProviderFileSystemStorage"
        raise NotImplementedError(msg)

    def get_provider_dir(self, provider_code: ProviderCode) -> Path:  # noqa: ARG002
        return self.storage_dir

    def iter_provider_directories(self, *, sort: bool = True) -> Iterator[Path]:  # noqa: ARG002
        yield self.storage_dir
