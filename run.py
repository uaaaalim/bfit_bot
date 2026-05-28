import asyncio
import logging

from bot import Client
from bot.core.logger import setup_logging
from startup import versions

logger = logging.getLogger(__name__)

async def run() -> None:
    setup_logging()
    logger.info("Environment variables are loaded")

    logger.info("Running Python {}".format(versions.python_version()))
    logger.info("Running '{}' version {}".format(versions.get_project_name(), versions.get_project_version()))
    logger.info("Authors: {}".format(versions.get_project_authors()))
    logger.info("Last commit: {}".format(versions.get_git_commit()))
    logger.info("-------------------------------------------------------")
    logger.info("aiogram: version {}".format(versions.aiogram_version()))
    logger.info("SQLAlchemy: version {}".format(versions.sqlalchemy_version()))
    logger.info("asyncpg: version {}".format(versions.asyncpg_version()))
    logger.info("alembic: version {}".format(versions.alembic_version()))
    logger.info("-------------------------------------------------------")

    logger.info("Loading bot components...")
    bot = Client()

    bot.load_routes()

    try:
        await bot.run()
    finally:
        await bot.shutdown()

if __name__ == '__main__':
    asyncio.run(run())