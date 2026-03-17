import asyncio
import platform
import subprocess

import aiogram
import alembic
import sqlalchemy

import core
from core.client import BotClient


def get_git_short_hash() -> str:
    try:
        return (
            subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], text=True)
            .strip()
        )
    except Exception:  # noqa: BLE001
        return "unknown"


async def main() -> None:
    client = BotClient()

    client.logger.info("[app] name=%s", core.__name__)
    client.logger.info("[app] version=%s", core.__version__)
    client.logger.info("[app] git=%s", get_git_short_hash())
    client.logger.info("[app] python=%s", platform.python_version())
    client.logger.info("[app] aiogram=%s", aiogram.__version__)
    client.logger.info("[app] sqlalchemy=%s", sqlalchemy.__version__)
    client.logger.info("[app] alembic=%s", alembic.__version__)

    try:
        await client.run()
    finally:
        await client.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
