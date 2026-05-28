from aiogram import Dispatcher

from handlers import ROUTERS
from middlewares.db import DatabaseMiddleware


def setup_middlewares(dp: Dispatcher, database_middleware: DatabaseMiddleware) -> None:
    dp.update.outer_middleware(database_middleware)


def setup_routers(dp: Dispatcher) -> None:
    for router in ROUTERS:
        dp.include_router(router)
