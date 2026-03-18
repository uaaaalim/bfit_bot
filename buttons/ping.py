from aiogram.types import CallbackQuery

from core.implementations.button import BaseButton


class PingButton(BaseButton):
    callback_data = "ping"

    async def execute(self, callback: CallbackQuery) -> None:
        await callback.answer("pong")
        await callback.message.answer("Кнопка Ping обработана ✅")
