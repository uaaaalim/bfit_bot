from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.core.cache.photo_cache import get_photo, save_photo_id
from utils.message_replace import remove_old_message

from .about import about_router
from .results import results_router

start_router = Router(name="start")
start_router.include_routers(about_router, results_router)

START_CAPTION = (
    "Здравствуйте. Это бот Ильи, персонального тренера 🏋️\n\n"
    "Здесь можно посмотреть результаты учеников, узнать об Илье "
    "и оставить заявку на подбор формата занятий.\n\n"
    "Хотите начать тренировки, вернуться в форму или понять, какой формат вам подойдёт? "
    "Заполните короткую анкету — Илья посмотрит вашу цель, опыт и возможные ограничения, "
    "после чего свяжется с вами лично."
)
START_BUTTONS = InlineKeyboardBuilder()

START_BUTTONS.button(text="🎯 Подобрать формат занятий", callback_data="start:survey")
START_BUTTONS.button(text="📸 Примеры работы", callback_data="start:results")
START_BUTTONS.button(text="🏆 Кто такой Илья", callback_data="start:about")

START_BUTTONS.adjust(1)


@start_router.message(CommandStart())
async def start_command(message: Message):
    sent_message = await message.answer_photo(
        photo=get_photo(message.bot.id, "main"),
        caption=START_CAPTION,
        reply_markup=START_BUTTONS.as_markup(),
    )
    save_photo_id(message.bot.id, "main", sent_message)

@start_router.callback_query(F.data == "start")
async def start_callback(callback: CallbackQuery):
    old_message = await remove_old_message(callback)
    sent_message = await old_message.answer_photo(
        photo=get_photo(callback.bot.id, "main"),
        caption=START_CAPTION,
        reply_markup=START_BUTTONS.as_markup(),
    )
    save_photo_id(callback.bot.id, "main", sent_message)

@start_router.callback_query(F.data == "start:survey")
async def start_survey(message: Message):
    pass
