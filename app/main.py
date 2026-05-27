import asyncio
import logging

from app.bot import create_bot, create_dispatcher
from config import get_settings
from config.logging import setup_logging
from database import create_db_engine

logger = logging.getLogger(__name__)


async def main() -> None:
    settings = get_settings()

    setup_logging(
        log_dir=settings.log_dir,
        level=settings.log_level,
        backup_count=settings.log_backup_count,
    )

    engine = create_db_engine(settings)

    bot = create_bot(settings)
    dp = create_dispatcher(engine)

    logger.info("Bot is starting")

    try:
        await dp.start_polling(bot)
    finally:
        logger.info("Bot is stopping")
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())