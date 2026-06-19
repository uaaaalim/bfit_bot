import logging

from app.bot.attachments import check_attachments
from app.bot.setup import create_bot, setup_dispatcher
from app.logger import setup_logging
from app.db.session import engine as db_engine

logger = logging.getLogger(__name__)


async def main() -> None:
    setup_logging()

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
