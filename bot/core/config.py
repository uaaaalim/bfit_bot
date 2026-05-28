import logging
from functools import lru_cache

from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)


class Configuration(BaseSettings):
    telegram_token: SecretStr = Field(alias="TELEGRAM_TOKEN")

    log_level: str = Field("INFO", alias="LOG_LEVEL")
    log_dir: str = Field("logs", alias="LOG_DIR")
    log_file_max_mb: int = Field(100, alias="LOG_FILE_MAX_MB")
    log_folder_max_mb: int = Field(1024, alias="LOG_FOLDER_MAX_MB")
    log_to_file: bool = Field(True, alias="LOG_TO_FILE")
    log_to_console: bool = Field(True, alias="LOG_TO_CONSOLE")

    database_host: str = Field(alias="DATABASE_HOST")
    database_port: int = Field(alias="DATABASE_PORT")
    database_user: str = Field(alias="DATABASE_USER")
    database_password: str = Field(alias="DATABASE_PASSWORD")
    database_name: str = Field(alias="DATABASE_DB")
    sql_echo: bool = Field(True, alias="SQL_ECHO")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    @property
    def database_url(self):
        return (f"postgresql+asyncpg://{self.database_user}:{self.database_password}@"
                f"{self.database_host}:{self.database_port}/{self.database_name}")

@lru_cache
def get_config() -> Configuration:
    return Configuration() # type: ignore

configuration = get_config()