from aiogram import Router

from app.bot.handlers.about import about_router
from app.bot.handlers.approach import approach_router
from app.bot.handlers.main import main_router
from app.bot.handlers.qualifications import qualifications_router

ROUTERS: list[Router] = [
    main_router,
    about_router,
    qualifications_router,
    approach_router
]