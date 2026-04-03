from aiogram.types import CallbackQuery

from core.implementations.button import BaseButton
from utils.main_menu import MAIN_MENU_TEXT, MAIN_MENU_KEYBOARD


class StartButton(BaseButton):
    callback_data = "menu:main"

    async def execute(self, callback: CallbackQuery) -> None:
        await callback.answer()
        await callback.message.edit_text(
            text=MAIN_MENU_TEXT,
            reply_markup=MAIN_MENU_KEYBOARD,
            parse_mode="HTML",
            disable_web_page_preview=True,
        )
