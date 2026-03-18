from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

MAIN_MENU_TEXT = (
    "👋 Привет еще раз! Я Илья - тренер.\n\n"
    "Перед началом тренировок хочу немного узнать тебя, "
    "чтобы сделать максимально эффективную и безопасную программу 💪\n\n"
    "➡️ Ответь, пожалуйста, на несколько простых вопросов:"
)

MAIN_MENU_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="📃 Заполнить анкету", callback_data="fill_form")]]
)


async def send_main_menu(bot: Bot, chat_id: int) -> Message:
    return await bot.send_message(
        chat_id=chat_id,
        text=MAIN_MENU_TEXT,
        parse_mode="HTML",
        reply_markup=MAIN_MENU_KEYBOARD,
    )
