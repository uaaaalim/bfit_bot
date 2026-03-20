from aiogram.types import CallbackQuery

from core.implementations.button import BaseButton
from utils.menu_page import send_menu_page


class DirectButton(BaseButton):
    callback_data = "menu:direct"

    async def execute(self, callback: CallbackQuery) -> None:
        if not callback.message:
            return

        await callback.message.delete()

        await send_menu_page(
            bot=self.client.bot,
            chat_id=callback.message.chat.id,
            text=(
                "️✍️ Написать в ЛС\n\n"
                "Вы также можете связаться со мной в личной переписке - @ilyamunfit"
            ),
        )
