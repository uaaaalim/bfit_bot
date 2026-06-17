import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from app.bot.middlewares.db import DbSessionMiddleware
from app.bot.routers import ROUTERS
from app.config import get_settings
from app.db import session_factory

settings = get_settings()
logger = logging.getLogger(__name__)


def create_bot() -> Bot:
    return Bot(
        token=settings.bot_token,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )

def setup_routers(dp: Dispatcher) -> None:
    for router in ROUTERS:
        dp.include_router(router)

    logger.info(f"{len(ROUTERS)} routers are loaded")

def setup_dispatcher() -> Dispatcher:
    dp = Dispatcher(storage=MemoryStorage())

    # middlewares
    dp.update.middleware(DbSessionMiddleware(session_factory=session_factory))

    # routers
    setup_routers(dp)

    return dp
