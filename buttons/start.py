from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from core.implementations.button import BaseButton


class StartButton(BaseButton):
    callback_data = "start_help"

    async def execute(self, callback: CallbackQuery) -> None:
        message = ("👋 Привет еще раз! Я Илья - тренер.\n\n"
                   "текст текст текст текст текст текст текст текст текст текст "
                   "текст текст текст текст текст текст текст текст текст текст "
                   "текст текст текст текст текст текст текст текст текст текст ")

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="📃 Заполнить анкету", callback_data="fill_form")]
            ]
        )

        await callback.message.delete()
        await callback.bot.send_message(callback.message.chat.id, message, parse_mode="HTML", reply_markup=keyboard)