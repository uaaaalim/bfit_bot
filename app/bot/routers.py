from aiogram import Router

from app.bot.handlers.about import about_router
from app.bot.handlers.approach import approach_router
from app.bot.handlers.contacts import contacts_router
from app.bot.handlers.main import main_router
from app.bot.handlers.qualifications import qualifications_router
from app.bot.handlers.results import results_router
from app.bot.handlers.survey import survey_router

ROUTERS: list[Router] = [
    main_router,
    about_router,
    qualifications_router,
    approach_router,
    results_router,
    survey_router,
    contacts_router
]