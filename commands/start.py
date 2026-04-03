from aiogram.types import Message

from core.implementations.command import BaseCommand
from utils.main_menu import MAIN_MENU_TEXT, MAIN_MENU_KEYBOARD


class StartCommand(BaseCommand):
    name = "start"
    description = "Запустить бота"

    async def execute(self, msg: Message) -> None:
        await msg.reply(
            text=MAIN_MENU_TEXT,
            reply_markup=MAIN_MENU_KEYBOARD,
            parse_mode="HTML",
            disable_web_page_preview=True,
        )
