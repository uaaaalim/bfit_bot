from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

results_router = Router(name="start.results")

async def reply_results(callback: CallbackQuery, page_before: str) -> None:
    keyboard = InlineKeyboardBuilder()

    message = (
        "Примеры работы\n\n"
        "Илья работает с разными задачами: снижение веса, набор мышечной массы, улучшение формы, тонус, "
        "возвращение к тренировкам и индивидуальные программы под график клиента.\n\n"
        "Ниже — несколько обезличенных примеров и историй учеников."
    )

    keyboard.button(text="🔥 Снижение веса", callback_data="start:results:weight")
    keyboard.button(text="⚖️ Форма и тонус", callback_data="start:results:body")
    keyboard.button(text="📊 Как отслеживается прогресс", callback_data="start:start:about:trains:progress")
    keyboard.button(text="🎯 Подобрать формат занятий", callback_data="start:survey")
    keyboard.button(text="⬅️ Назад", callback_data=f"start{page_before}")

    keyboard.adjust(2, 1)

    await callback.message.edit_text(text=message, reply_markup=keyboard.as_markup())

@results_router.callback_query(F.data == "start:results_from_start")
async def results_from_start(callback: CallbackQuery):
    await reply_results(callback, "")

@results_router.callback_query(F.data == "start:results_from_about_trains_mtr10")
async def results_from_trains_mtr10(callback: CallbackQuery):
    await reply_results(callback, ":about:trains:mtr10")

@results_router.callback_query(F.data == "start:results_from_about_trains_progress")
async def results_from_trains_progress(callback: CallbackQuery):
    await reply_results(callback, ":about:trains:progress")

@results_router.callback_query(F.data == "results_from_about")
async def results_from_about(callback: CallbackQuery):
    await reply_results(callback, ":about")
