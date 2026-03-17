import os

from dotenv import load_dotenv


class Config:
    def __init__(self, bot_token: str, database_url: str, log_level: str = "INFO") -> None:
        self.bot_token = bot_token
        self.database_url = database_url
        self.log_level = log_level


def load_config() -> Config:
    load_dotenv()

    bot_token = os.getenv("BOT_TOKEN", "")
    if not bot_token:
        raise ValueError("BOT_TOKEN is required in .env")

    database_url = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres@localhost:5432/bfit_bot",
    )
    log_level = os.getenv("LOG_LEVEL", "INFO")
    return Config(bot_token=bot_token, database_url=database_url, log_level=log_level)
