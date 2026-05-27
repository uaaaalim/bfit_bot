import asyncio
import logging

from app.bot import initialize_bot
from config import get_settings
from config.logging import setup_logging
from utils.project_info import build_short_startup_info

logger = logging.getLogger(__name__)


async def main() -> None:
    settings = get_settings()

    setup_logging(
        log_dir=settings.log_dir,
        level=settings.log_level,
        backup_count=settings.log_backup_count,
    )

    for log in build_short_startup_info():
        logger.info(log)

    await initialize_bot(settings)

if __name__ == "__main__":
    asyncio.run(main())