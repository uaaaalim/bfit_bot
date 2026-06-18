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
            "Илья Мун — персональный тренер, КМС по бодибилдингу, "
            "автор книг о фитнесе и создатель тренировочной системы MTR 10.\n\n"
            "В фитнесе с 2011 года. Илья работает с мужчинами и женщинами разного уровня подготовки: "
            "от новичков до тех, кто уже тренируется, но хочет более понятную систему и стабильный результат.\n\n"
            "Главный принцип работы — не давать всем одну и ту же программу, а подбирать тренировки под цель, "
            "опыт, ограничения и реальный образ жизни человека."
        ),
        reply_markup=keyboard.as_markup(),
    )
