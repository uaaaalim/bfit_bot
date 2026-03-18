from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from core.implementations.button import BaseButton


class DirectButton(BaseButton):
    callback_data = "menu:direct"

    async def execute(self, callback: CallbackQuery) -> None:
        await callback.message.delete()

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="⬅️ Вернуться в главное меню", callback_data="menu:main")
                ]
            ]
        )

        await self.client.bot.send_message(
            callback.message.chat.id,
            "️✍️ Написать в ЛС\n\n"
            "Вы также можете связаться со мной в личной переписке - @ilyamunfit",
            reply_markup=keyboard,
            parse_mode="HTML"
        )