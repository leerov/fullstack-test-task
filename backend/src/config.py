from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env.dev", env_file_encoding="utf-8")

    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "backend-db"
    POSTGRES_DB: str = "postgres"
    PGPORT: int = 5432

    REDIS_URL: str = "redis://backend-redis:6379/0"

    MAX_FILE_SIZE_BYTES: int = 10 * 1024 * 1024

    STORAGE_PATH: str = str(Path(__file__).resolve().parent.parent / "storage" / "files")

    @property
    def db_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.PGPORT}/{self.POSTGRES_DB}"
        )


settings = Settings()