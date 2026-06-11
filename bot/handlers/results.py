from aiogram import Router, F
from aiogram.types import CallbackQuery, InputMediaPhoto
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.core.cache.photo_cache import get_photo, save_photo_id

results_router = Router(name="start.results")

@results_router.callback_query(F.data == "start:results")
async def results(callback: CallbackQuery):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="➡️ Следующий", callback_data="start:results:1")
    keyboard.button(text="🏆 Узнать о подходе Ильи", callback_data="start:about")
    keyboard.button(text="⬅️ Назад в главное меню", callback_data="start")
    keyboard.adjust(1)

    await callback.answer()
    edited_message = await callback.message.edit_media(
        media=InputMediaPhoto(media=get_photo(callback.bot.id, "doc_0")),
        reply_markup=keyboard.as_markup(),
    )
    save_photo_id(callback.bot.id, "doc_0", edited_message)


