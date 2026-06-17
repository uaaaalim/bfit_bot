import logging

from app.logger import setup_logging

logger = logging.getLogger(__name__)


async def main() -> None:
    setup_logging()

    logger.info("SIX SEVEEEN")
