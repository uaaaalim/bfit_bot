from aiogram.types import CallbackQuery

from core.implementations.button import BaseButton


class FillFormButton(BaseButton):
    callback_data = "fill_form"

    async def execute(self, callback: CallbackQuery) -> None:
        pass