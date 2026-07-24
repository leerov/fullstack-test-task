import os
import shutil
from pathlib import Path

from src.config import settings
from src.storage.base import StorageProvider


class LocalStorageProvider(StorageProvider):
    def __init__(self) -> None:
        self.base_dir = Path(settings.STORAGE_PATH).resolve()
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _sanitize_filename(self, filename: str) -> str:
        # Prevent path traversal attacks
        basename = os.path.basename(filename)
        # Allow only alphanumeric, dots, hyphens, and underscores
        if not all(c.isalnum() or c in '.-_' for c in basename):
            raise ValueError(f"Invalid filename: {filename}")
        return basename

    def save(self, filename: str, content: bytes) -> str:
        safe_filename = self._sanitize_filename(filename)
        file_path = self.base_dir / safe_filename
        file_path.write_bytes(content)
        return str(file_path)

    def save_file(self, filename: str, src_path: Path) -> str:
        safe_filename = self._sanitize_filename(filename)
        file_path = self.base_dir / safe_filename
        shutil.copy2(src_path, file_path)
        return str(file_path)

    def delete(self, filename: str) -> None:
        safe_filename = self._sanitize_filename(filename)
        file_path = self.base_dir / safe_filename
        if file_path.exists():
            file_path.unlink()

    def get_path(self, filename: str) -> Path:
        safe_filename = self._sanitize_filename(filename)
        return self.base_dir / safe_filename