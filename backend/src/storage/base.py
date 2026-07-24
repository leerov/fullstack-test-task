from abc import ABC, abstractmethod
from pathlib import Path


class StorageProvider(ABC):
    @abstractmethod
    def save(self, filename: str, content: bytes) -> str:
        pass

    @abstractmethod
    def save_file(self, filename: str, src_path: Path) -> str:
        pass

    @abstractmethod
    def delete(self, filename: str) -> None:
        pass

    @abstractmethod
    def get_path(self, filename: str) -> Path:
        pass