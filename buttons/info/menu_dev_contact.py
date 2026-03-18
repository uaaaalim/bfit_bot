from aiogram.types import CallbackQuery

from core.implementations.button import BaseButton
from utils.menu_page import send_menu_page


class DevContactButton(BaseButton):
    callback_data = "menu:dev_contact"

    async def execute(self, callback: CallbackQuery) -> None:
        if not callback.message:
            return

        await callback.message.delete()

        await send_menu_page(
            bot=self.client.bot,
            chat_id=callback.message.chat.id,
            text=(
                "️❓ Связь с разработчиком\n\n"
                "Данный бот был разработан по заказу для Ильи без использования конструкторов и ИИ.\n"
                "По ошибкам, предложениям и заказам вы можете обратиться к @uaaaalim\n\n"
                "💖 Сделано с душой и с любовью на языке Python 3.13 🐍"
            ),
        )
