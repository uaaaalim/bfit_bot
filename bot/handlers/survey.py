from aiogram import Router, F
from aiogram.types import CallbackQuery

survey_router = Router(name='start.survey')

@survey_router.callback_query(F.data == "start:survey")
async def start_survey(callback: CallbackQuery):
    pass