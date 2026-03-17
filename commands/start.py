from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from core.implementations.command import BaseCommand


class StartCommand(BaseCommand):
    name = "start"
    description = "Запуск бота"

    async def execute(self, message: Message) -> None:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Ping", callback_data="ping")],
                [InlineKeyboardButton(text="Ждать кнопку 10 сек", callback_data="demo_wait_button")],
            ]
        )
        await message.answer(
            "Привет! Доступно:\n"
            "/wait_message - ждать сообщение 10 сек\n"
            "/db_demo - создать/получить пользователя\n"
            "Или нажми кнопку ниже.",
            reply_markup=keyboard,
        )
