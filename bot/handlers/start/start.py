from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.utils.keyboard import InlineKeyboardBuilder

from attachments import PHOTOS

from .about import about_router

start_router = Router(name="start")
start_router.include_routers(about_router)

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
START_BUTTONS.button(text="📸 Результаты учеников", callback_data="start:results")
START_BUTTONS.button(text="🏆 Кто такой Илья", callback_data="start:about")

START_BUTTONS.adjust(1)


@start_router.message(CommandStart())
async def start_command(message: Message):
    await message.answer_photo(
        photo=PHOTOS['IMG_4597.JPG'],
        caption=START_CAPTION,
        reply_markup=START_BUTTONS.as_markup(),
    )

@start_router.callback_query(F.data == "start")
async def start_callback(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_media(
        media=InputMediaPhoto(media=PHOTOS['IMG_4597.JPG'], caption=START_CAPTION),
        reply_markup=START_BUTTONS.as_markup(),
    )

@start_router.callback_query(F.data == "start:survey")
async def start_survey(message: Message):
    pass

@start_router.callback_query(F.data == "start:results")
async def start_results(message: Message):
    pass

@start_router.callback_query(F.data == "start:about")
async def start_about(callback: CallbackQuery):
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="🎓 Образование и квалификация", callback_data="start:about:education")
    keyboard.button(text="📘 Подход к тренировкам", callback_data="start:about:trains")
    keyboard.button(text="📸 Результаты учеников", callback_data="start:results")
    keyboard.button(text="🎯 Подобрать формат занятий", callback_data="start:survey")
    keyboard.button(text="⬅️ Назад", callback_data="start")

    keyboard.adjust(2, 1)

    await callback.answer()
    await callback.message.edit_media(
        media=InputMediaPhoto(
            media=FSInputFile("attachments/photo/photo_2026-05-31_23-16-00.jpg"),
            caption=(
                "Илья Мун — персональный тренер, КМС по бодибилдингу, "
                "автор книг о фитнесе и создатель тренировочной системы MTR 10.\n\n"
                "В фитнесе с 2011 года. Работает с людьми разного уровня: от новичков до тех, кто уже тренируется, "
                "но не видит стабильного результата.\n\n"
                "Главный принцип работы — не давать всем одну и ту же программу, а подбирать тренировки под цель, "
                "опыт, ограничения и реальный образ жизни человека."
            ),
        ),
        reply_markup=keyboard.as_markup(),
    )
