from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_token: str = Field(alias="BOT_TOKEN")

    postgres_host: str = Field(alias="POSTGRES_HOST", default="localhost")
    postgres_port: int = Field(alias="POSTGRES_PORT", default=5432)
    postgres_user: str = Field(alias="POSTGRES_USER")
    postgres_password: str = Field(alias="POSTGRES_PASSWORD")
    postgres_db: str = Field(alias="POSTGRES_DB")

    log_level: str = Field(alias="LOG_LEVEL", default="INFO")
    log_dir: Path = Field(alias="LOG_DIR", default=Path("logs"))
    log_backup_count: int = Field(alias="LOG_BACKUP_COUNT", default=100)

    admins_raw: str = Field(alias="ADMINS")

    @property
    def admins(self) -> list[int]:
        return list(map(int, self.admins_raw.split(",")))

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:"
            f"{self.postgres_password}@{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def alembic_database_url(self) -> str:
        return (
            f"postgresql+psycopg://{self.postgres_user}:"
            f"{self.postgres_password}@{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_db}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings() # type: ignore[call-arg]