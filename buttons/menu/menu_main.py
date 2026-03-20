from aiogram.types import CallbackQuery

from core.implementations.button import BaseButton
from utils.main_menu import send_main_menu


class StartButton(BaseButton):
    callback_data = "menu:main"

    async def execute(self, callback: CallbackQuery) -> None:
        if callback.message:
            await callback.message.delete()
            await send_main_menu(callback.bot, callback.message.chat.id)
