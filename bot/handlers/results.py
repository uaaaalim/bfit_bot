from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

results_router = Router(name="start.results")

@results_router.callback_query(F.data == "start:results")
async def results(callback: CallbackQuery):
    keyboard = InlineKeyboardBuilder()

    message = (
        "Примеры работы\n\n"
        "Илья работает с разными задачами: снижение веса, набор мышечной массы, улучшение формы, тонус, "
        "возвращение к тренировкам и индивидуальные программы под график клиента.\n\n"
        "Ниже — несколько обезличенных примеров и историй учеников."
    )

    keyboard.button(text="🔥 Снижение веса", callback_data="start:results:weight")
    keyboard.button(text="⚖️ Форма и тонус", callback_data="start:results:body")
    keyboard.button(text="📊 Как отслеживается прогресс", callback_data="start:about:trains:progress")
    keyboard.button(text="🎯 Подобрать формат занятий", callback_data="start:survey")
    keyboard.button(text="🏆 Кто такой Илья", callback_data="start:about")

    keyboard.adjust(2, 1)

    await callback.message.edit_caption(caption=message, reply_markup=keyboard.as_markup())
