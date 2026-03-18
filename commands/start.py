from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from core.implementations.command import BaseCommand


class StartCommand(BaseCommand):
    name = "start"
    description = "Запустить бота"

    async def execute(self, msg: Message) -> None:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🏃‍♂️ СТАРТ!", callback_data="start_help")]
            ]
        )

        await msg.reply("👋 Привет! Я помощник тренера.\n"
                        "➡️ Если ты хочешь <b>стать лучше</b> нажми "
                        "<b>СТАРТ!</b> ниже!", reply_markup=keyboard, parse_mode="HTML")
