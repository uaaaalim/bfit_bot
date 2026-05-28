import logging

from aiogram import Dispatcher

from bot.core.database import session_maker
from bot.handlers import ROUTERS
from bot.middlewares.database import DatabaseMiddleware
from bot import Client

logger = logging.getLogger(__name__)


async def load(client: Client) -> None:
    """ Loads all routers (NECESSARY FUNCTION // DON'T REMOVE IT) """
    await load_routers(client.dp)
    await load_middlewares(client.dp)

async def load_routers(dp: Dispatcher) -> None:
    for router in ROUTERS:
        dp.include_router(router)

    logger.info("{} routers are loaded".format(len(ROUTERS)))

async def load_middlewares(dp: Dispatcher) -> None:
    dp.update.middleware(DatabaseMiddleware(session_maker=session_maker))

    logger.info("All middlewares are loaded")
