from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.cache.attachments import AttachmentsMemoryCache
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
MAIN_BUTTONS.button(text="🎯 Подобрать формат занятий", callback_data="start:survey")
MAIN_BUTTONS.button(text="📸 Примеры работы", callback_data="start:results")
MAIN_BUTTONS.button(text="🏆 Кто такой Илья", callback_data="start:about")
MAIN_BUTTONS.adjust(1)


@main_router.message(CommandStart)
async def start_command(message: types.Message, attachments_cache: AttachmentsMemoryCache) -> None:
    await message.answer_photo(
        photo=attachments_cache.get("app/attachments/images/main_menu.jpg"),
        caption=MAIN_MESSAGE,
        reply_markup=MAIN_BUTTONS.as_markup(),
    )

@main_router.callback_query(F.data == "main_menu")
async def start_button(callback: CallbackQuery, attachments_cache: AttachmentsMemoryCache) -> None:
    old_message = await remove_old_message(callback)

    await old_message.answer_photo(
        photo=attachments_cache.get("app/attachments/images/main_menu.jpg"),
        caption=MAIN_MESSAGE,
        reply_markup=MAIN_BUTTONS.as_markup(),
    )
    await callback.answer()
