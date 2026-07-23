from pathlib import Path

from src.storage.base import StorageProvider


class LocalStorageProvider(StorageProvider):
    def __init__(self) -> None:
        self.base_dir = Path(__file__).resolve().parent.parent.parent / "storage" / "files"
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def save(self, filename: str, content: bytes) -> str:
        file_path = self.base_dir / filename
        file_path.write_bytes(content)
        return str(file_path)

    def delete(self, filename: str) -> None:
        file_path = self.base_dir / filename
        if file_path.exists():
            file_path.unlink()

    def get_path(self, filename: str) -> Path:
        return self.base_dir / filename