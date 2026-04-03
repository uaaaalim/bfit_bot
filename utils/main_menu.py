from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

MAIN_MENU_TEXT = """
👋 Привет. Я Илья — тренер с опытом более <b>15 лет</b>.

Если коротко:
ты не получаешь результат не потому что ленивый

А потому что:
— нет системы
— нет контроля
— нет понимания, что реально работает

Работаю не “на процесс”, а на <b>результат</b>:
— похудение
— набор массы
— исправление осанки

📊 Более <b>100+ клиентов</b> уже изменили свое тело

Я также написал практическую книгу по фитнесу, где объясняю, почему у большинства не получается добиться результата.

👇 Выбери, с чего хочешь начать:
"""

MAIN_MENU_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🔥 Хочу результат!", callback_data="menu:wants_result")
        ],
        [
            InlineKeyboardButton(text="🎁 Забрать Подарок", callback_data="menu:gift"),
        ],
        [
            InlineKeyboardButton(text="📖 Моя книга", callback_data="menu:my_book"),
            InlineKeyboardButton(text="📊 Результаты", callback_data="menu:results")
        ],
        [
            InlineKeyboardButton(text="👨‍🏫 Обо мне", callback_data="menu:about_me"),
            InlineKeyboardButton(text="❓ Вопросы", callback_data="menu:questions")
        ],
        [
            InlineKeyboardButton(text="💪 Программы", callback_data="menu:programs"),
            InlineKeyboardButton(text="💬 Написать мне", callback_data="menu:contact_me")
        ]
    ]
)

def get_page_buttons():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Вернуться на главную страницу", callback_data="menu:main")],
        ]
    )
