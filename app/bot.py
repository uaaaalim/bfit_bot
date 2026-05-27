import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from sqlalchemy.ext.asyncio import AsyncEngine

from config import Settings
from database import create_session_maker, create_db_engine
from handlers import ROUTERS
from middlewares.db import DatabaseMiddleware

logger = logging.getLogger(__name__)


async def initialize_bot(settings: Settings):
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
        ),
    )

    dp = Dispatcher()

    db_engine = create_db_engine(settings)
    session_maker = create_session_maker(db_engine)

    dp.update.outer_middleware(DatabaseMiddleware(session_maker))
    for router in ROUTERS:
        dp.include_router(router)

    try:
        await start_bot(bot, dp)
    finally:
        await shutdown(bot, dp, db_engine)

async def start_bot(bot: Bot, dp: Dispatcher):
    logger.info("Starting up...")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

async def shutdown(bot: Bot, dp: Dispatcher, db: AsyncEngine):
    logger.info("Shutting down...")

    await bot.session.close()
    await dp.storage.close()
    await db.dispose()
