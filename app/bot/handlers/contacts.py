from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.cache import attachments_cache
from app.utils.message_resolver import remove_old_message

contacts_router = Router(name="contacts")

@contacts_router.callback_query(F.data == "contacts")
async def contacts(callback: CallbackQuery):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(url="https://t.me/ilyamunfit", text="Связаться в Telegram")
    keyboard.button(url="https://instagram.com/ilyamun.fit", text="Страничка в Instagram")
    keyboard.button(url="https://tiktok.com/@ilyamunfit2", text="Я в TikTok")
    keyboard.button(url="https://t.me/uaaaalim", text="Разработчик этого бота")
    keyboard.button(text="⬅️ Назад", callback_data="about")
    keyboard.adjust(1)

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
