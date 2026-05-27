from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from sqlalchemy.ext.asyncio import AsyncEngine

from config import Settings
from database import create_session_maker
from middlewares.db import DatabaseMiddleware


def create_bot(settings: Settings) -> Bot:
    return Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
        ),
    )


def create_dispatcher(engine: AsyncEngine) -> Dispatcher:
    dp = Dispatcher()

    session_maker = create_session_maker(engine)

    dp.update.middleware(DatabaseMiddleware(session_maker))

    return dp