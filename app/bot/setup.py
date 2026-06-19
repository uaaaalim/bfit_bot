import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from app.bot.middlewares.db import DbSessionMiddleware
from app.bot.middlewares.user import UserCheckMiddleware
from app.bot.routers import ROUTERS
from app.config import get_settings
from app.db import session_factory

settings = get_settings()
logger = logging.getLogger(__name__)


def create_bot() -> Bot:
    return Bot(
        token=settings.bot_token.get_secret_value(),
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
            link_preview_is_disabled=True
        )
    )

def _setup_routers(dp: Dispatcher) -> None:
    for router in ROUTERS:
        dp.include_router(router)

    logger.info(f"{len(ROUTERS)} routers are loaded")

def setup_dispatcher() -> Dispatcher:
    dp = Dispatcher(storage=MemoryStorage())

    # middlewares
    dp.update.middleware(DbSessionMiddleware(session_factory=session_factory))
    dp.update.middleware(UserCheckMiddleware())

    # routers
    _setup_routers(dp)

    return dp
