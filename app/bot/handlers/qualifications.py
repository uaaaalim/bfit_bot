from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.bot.cache import attachments_cache

qualifications_router = Router(name="qualifications")

@qualifications_router.callback_query(F.data == "qualifications")
async def qualifications_button(callback: CallbackQuery):
    pass