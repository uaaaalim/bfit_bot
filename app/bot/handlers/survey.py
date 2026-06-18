from aiogram import Router, F
from aiogram.types import CallbackQuery

survey_router = Router(name="survey")

@survey_router.callback_query(F.data == "survey")
async def survey_button(callback: CallbackQuery):
    pass
