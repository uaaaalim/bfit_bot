import logging
import sys

from app.bot.attachments import check_attachments
from app.bot.setup import create_bot, setup_dispatcher
from app.logger import setup_logging
from app.db.session import engine as db_engine
from app.utils.project_info import project_name, project_version, project_authors

logger = logging.getLogger(__name__)


async def main() -> None:
    setup_logging()

    logger.info(f"Running python version {'.'.join(map(str, sys.version_info[:3]))}")
    logger.info(f"Loading project {project_name} version {project_version}")
    logger.info(f"Developed by {project_authors}")

    logger.info("Loading bot parameters...")

    bot = create_bot()
    dp = setup_dispatcher()

    try:
        logger.info("Checking cached attachments...")
        await check_attachments(bot)

        logger.info("Connecting to Telegram...")
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as e:
        logger.exception("An error occurred while running: %s", e)
    finally:
        await bot.session.close()
        await db_engine.dispose()

        logger.warning("All connections are closed.")
