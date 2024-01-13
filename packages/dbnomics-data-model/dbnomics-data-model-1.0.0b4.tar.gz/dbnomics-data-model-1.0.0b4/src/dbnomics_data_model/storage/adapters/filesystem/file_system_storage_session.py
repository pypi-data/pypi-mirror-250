import shutil
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Self

import daiquiri

from dbnomics_data_model.file_utils import write_gitignore_all
from dbnomics_data_model.storage.adapters.filesystem.constants import BASE_SESSION_DIR_NAME
from dbnomics_data_model.storage.adapters.filesystem.errors.file_system_storage import StorageDirectoryNotFound
from dbnomics_data_model.storage.adapters.filesystem.errors.file_system_storage_session import SessionDirectoryNotFound
from dbnomics_data_model.storage.adapters.filesystem.file_system_storage import FileSystemStorage
from dbnomics_data_model.storage.adapters.filesystem.file_utils import move_children
from dbnomics_data_model.storage.errors.storage_session import StorageSessionNeverEntered
from dbnomics_data_model.storage.storage_session import StorageSession

if TYPE_CHECKING:
    from dbnomics_data_model.storage.adapters.filesystem.file_system_storage_uri import FileSystemStorageUri


__all__ = ["FileSystemStorageSession"]


logger = daiquiri.getLogger(__name__)


class FileSystemStorageSession(StorageSession):
    def __init__(
        self, *, name: str | None = None, session_dir: Path, storage: FileSystemStorage, storage_dir: Path
    ) -> None:
        super().__init__(name=name, storage=storage)

        if not session_dir.is_dir():
            raise SessionDirectoryNotFound(session_dir=session_dir)
        self.session_dir = session_dir

        if not storage_dir.is_dir():
            raise StorageDirectoryNotFound(storage_dir=storage_dir)
        self.storage_dir = storage_dir

    @classmethod
    def from_uri(cls, uri: "FileSystemStorageUri", *, session_name: str | None = None) -> Self:  # type: ignore[override]
        storage_dir = uri.path
        session_dir = cls._create_session_dir(session_dir_name=session_name, storage_dir=storage_dir)
        new_uri = replace(uri, path=session_dir)
        storage = FileSystemStorage.from_uri(new_uri)
        return cls(session_dir=session_dir, storage=storage, storage_dir=storage_dir)

    def commit(self) -> None:
        super().commit()

        if not self._has_entered:
            raise StorageSessionNeverEntered(storage_session=self)

        move_children(self.session_dir, self.storage_dir, overwrite=True)
        logger.debug(
            "Committed session %s by moving files from %s to %s", self.name, self.session_dir, self.storage_dir
        )

    def rollback(self) -> None:
        pass

    @classmethod
    def _create_base_session_dir(cls, *, storage_dir: Path) -> Path:
        base_session_dir = storage_dir / BASE_SESSION_DIR_NAME
        base_session_dir.mkdir(exist_ok=True)
        write_gitignore_all(base_session_dir, exist_ok=True)
        return base_session_dir

    @classmethod
    def _create_session_dir(cls, *, session_dir_name: str | None = None, storage_dir: Path) -> Path:
        base_session_dir = cls._create_base_session_dir(storage_dir=storage_dir)

        if session_dir_name is None:
            session_dir_name = datetime.isoformat(datetime.now(tz=timezone.utc))

        session_dir = base_session_dir / session_dir_name
        session_dir_exists = session_dir.is_dir()
        if session_dir_exists:
            shutil.rmtree(session_dir)
        session_dir.mkdir()
        logger.debug("%s session directory: %s", "Recreated" if session_dir_exists else "Created", session_dir)

        return session_dir
