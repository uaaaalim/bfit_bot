from aiogram.types import Message

from core.implementations.command import BaseCommand
from utils.main_menu import send_main_menu


class StartCommand(BaseCommand):
    name = "start"
    description = "Запустить бота"

    async def execute(self, msg: Message) -> None:
        await send_main_menu(msg.bot, msg.chat.id)
