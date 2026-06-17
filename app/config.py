from functools import lru_cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_token: SecretStr = Field(alias="BOT_TOKEN")

    log_dir: str = Field(default="./logs", alias="LOG_DIR")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    log_file_max_mb: int = Field(default=1024, alias="LOG_FILE_MAX_MB")
    log_folder_max_mb: int = Field(default=1024, alias="LOG_FOLDER_MAX_MB")
    log_to_console: bool = Field(default=True, alias="LOG_TO_CONSOLE")
    log_to_file: bool = Field(default=True, alias="LOG_TO_FILE")

    postgres_host: str = Field(alias="POSTGRES_HOST")
    postgres_port: str = Field(alias="POSTGRES_PORT")
    postgres_user: str = Field(alias="POSTGRES_USER")
    postgres_password: str = Field(alias="POSTGRES_PASSWORD")
    postgres_db: str = Field(alias="POSTGRES_DB")

    admin_ids: str = Field(default="", alias="ADMIN_IDS")
    media_check_victim_id: int = Field(alias="MEDIA_CHECK_VICTIM_ID")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def database_url(self) -> str:
        return (f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
                f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}")

    @property
    def admin_id_list(self) -> list[int]:
        if not self.admin_ids:
            return []

        return [
            int(admin_id.strip())
            for admin_id in self.admin_ids.split(",")
            if admin_id.strip()
        ]

@lru_cache
def get_settings() -> Settings:
    return Settings() # type: ignore
