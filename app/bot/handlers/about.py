from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.cache import attachments_cache
from app.utils.message_resolver import remove_old_message

about_router = Router(name="about")

@about_router.callback_query(F.data == "about")
async def about_button(callback: CallbackQuery) -> None:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🎓 Образование и квалификация", callback_data="qualifications")
    keyboard.button(text="📘 Подход к тренировкам", callback_data="about:approach")
    keyboard.button(text="📸 Примеры работы", callback_data="about:results:1")
    keyboard.button(text="📕 Контакты", callback_data="contacts")
    keyboard.button(text="🎯 Подобрать формат занятий", callback_data="survey")
    keyboard.adjust(2, 2, 1)

    await callback.answer()
    old_message = await remove_old_message(callback)
    await old_message.answer_photo(
        photo=attachments_cache.get("app/attachments/about.jpg"),
        caption=(
            "Контакты.\n\n"
            "Здесь сборник социальных сетей Ильи, подписывайтесь, делитесь мнением, задавайте вопросы!\n"
            "Также, вы можете обратиться к нему лично, написав в личные сообщения."
        ),
        reply_markup=keyboard.as_markup(),
    )
