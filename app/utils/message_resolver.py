from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, Message


async def remove_old_message(callback: CallbackQuery) -> Message:
    message = callback.message
    if message is None:
        raise RuntimeError("Callback query has no message")

    try:
        await message.delete()
    except TelegramBadRequest:
        try:
            await message.edit_reply_markup(reply_markup=None)
        except TelegramBadRequest:
            pass

    return message
