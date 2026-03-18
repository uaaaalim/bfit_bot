from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from core.implementations.button import BaseButton


class DevContactButton(BaseButton):
    callback_data = "menu:dev_contact"

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
            "️❓ Связь с разработчиком\n\n"
            "Данный бот был разработан по заказу для Ильи без использования конструкторов и ИИ.\n"
            "По ошибкам, предложениям и заказам вы можете обратиться к @uaaaalim\n\n"
            "💖 Сделано с душой и с любовью на языке Python 3.13 🐍",
            reply_markup=keyboard,
            parse_mode="HTML"
        )