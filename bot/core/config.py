from functools import lru_cache

from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Configuration(BaseSettings):
    telegram_token: SecretStr = Field(alias="TELEGRAM_TOKEN")

    log_level: str = Field("INFO", alias="LOG_LEVEL")
    log_dir: str = Field("logs", alias="LOG_DIR")
    log_file_max_mb: int = Field(100, alias="LOG_FILE_MAX_MB")
    log_folder_max_mb: int = Field(1024, alias="LOG_FOLDER_MAX_MB")
    log_to_file: bool = Field(True, alias="LOG_TO_FILE")
    log_to_console: bool = Field(True, alias="LOG_TO_CONSOLE")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

@lru_cache
def get_config() -> Configuration:
    return Configuration() # type: ignore

configuration = get_config()