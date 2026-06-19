from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.cache import attachments_cache
from app.utils.message_resolver import remove_old_message

main_router = Router(name="start")

MAIN_MESSAGE = (
    "Здравствуйте. Это бот Ильи, персонального тренера 🏋️\n\n"
    "Здесь можно посмотреть результаты учеников, узнать об Илье "
    "и оставить заявку на подбор формата занятий.\n\n"
    "Хотите начать тренировки, вернуться в форму или понять, какой формат вам подойдёт? "
    "Заполните короткую анкету — Илья посмотрит вашу цель, опыт и возможные ограничения, "
    "после чего свяжется с вами лично."
)

MAIN_BUTTONS = InlineKeyboardBuilder()
MAIN_BUTTONS.button(text="🎯 Подобрать формат занятий", callback_data="survey")
MAIN_BUTTONS.button(text="📸 Примеры работы", callback_data="main_menu:results:1")
MAIN_BUTTONS.button(text="🏆 Кто такой Илья", callback_data="about")
MAIN_BUTTONS.adjust(1)


@main_router.message(CommandStart())
async def start_command(message: types.Message) -> None:
    await message.answer_photo(
        photo=attachments_cache.get("app/attachments/main_menu.jpg"),
        caption=MAIN_MESSAGE,
        reply_markup=MAIN_BUTTONS.as_markup(),
    )

@main_router.callback_query(F.data == "main_menu")
async def start_button(callback: CallbackQuery) -> None:
    await callback.answer()
    old_message = await remove_old_message(callback)
    await old_message.answer_photo(
        photo=attachments_cache.get("app/attachments/main_menu.jpg"),
        caption=MAIN_MESSAGE,
        reply_markup=MAIN_BUTTONS.as_markup(),
    )
    await callback.answer()
