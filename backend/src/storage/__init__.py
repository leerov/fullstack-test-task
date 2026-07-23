from src.storage.base import StorageProvider
from src.storage.local import LocalStorageProvider

storage_provider: StorageProvider = LocalStorageProvider()