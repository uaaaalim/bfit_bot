from aiogram import Router

from app.bot.handlers.main import main_router

ROUTERS: list[Router] = [
    main_router
]