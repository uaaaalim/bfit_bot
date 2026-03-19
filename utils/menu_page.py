from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def send_menu_page(
    bot: Bot,
    chat_id: int,
    text: str,
    *,
    include_fill_form: bool = False,
) -> None:
    keyboard_rows = []

    if include_fill_form:
        keyboard_rows.append(
            [InlineKeyboardButton(text="📃 Заполнить анкету", callback_data="menu:fill_form")]
        )

    keyboard_rows.append(
        [InlineKeyboardButton(text="⬅️ Вернуться в главное меню", callback_data="menu:main")]
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_rows)
    await bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=keyboard,
        parse_mode="HTML",
    )
