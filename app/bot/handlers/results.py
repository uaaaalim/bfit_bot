from aiogram import Router, F
from aiogram.types import CallbackQuery

results_router = Router(name="results")

@results_router.callback_query(F.data == "results")
async def results_button(callback: CallbackQuery) -> None:
    pass
