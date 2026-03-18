from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

MAIN_MENU_TEXT = (
    "👋 Привет. Я Илья — тренер с опытом более 15 лет.\n\n"

    "Работаю на результат: похудение, набор массы, бокс и исправление осанки (сколиоз и сутулость).\n\n"

    "👇 Выбирай:\n"
    "• Обо мне — кто я и как работаю\n"
    "• Написать в ЛС — связаться со мной\n"
    "• Заполнить анкету — начать тренировки\n"
)

MAIN_MENU_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="👤 Обо мне", callback_data="menu:about_me"),
            InlineKeyboardButton(text="✍️ Написать в ЛС", callback_data="menu:direct")
        ],
        [
            InlineKeyboardButton(text="📃 Заполнить анкету", callback_data="menu:fill_form")
        ],
        [
            InlineKeyboardButton(text="❓ Связь с разработчиком", callback_data="menu:dev_contact")
        ]
    ]
)


async def send_main_menu(bot: Bot, chat_id: int) -> Message:
    return await bot.send_message(
        chat_id=chat_id,
        text=MAIN_MENU_TEXT,
        parse_mode="HTML",
        reply_markup=MAIN_MENU_KEYBOARD,
    )
