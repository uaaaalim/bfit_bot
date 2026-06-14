from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.core.active_action import finish_action, get_active_action, has_active_action, start_action
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
async def start_survey(callback: CallbackQuery):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="✅ Продолжить", callback_data="survey:continue")
    keyboard.adjust(1)

    old_message = await remove_old_message(callback)
    await old_message.answer(
        "Нажмите кнопку в течение 30 секунд, чтобы начать короткую анкету.",
        reply_markup=keyboard.as_markup(),
    )
    start_action(
        bot=callback.bot,
        user_id=callback.from_user.id,
        kind="button",
        timeout=30,
        callback_data="survey:continue",
        on_timeout=survey_button_timeout,
    )


@start_router.callback_query(F.data == "survey:continue")
async def continue_survey(callback: CallbackQuery):
    action = get_active_action(callback.from_user.id)
    if action is None or action.kind != "button":
        await callback.answer("Эта кнопка уже не активна.", show_alert=True)
        return

    finish_action(callback.from_user.id)
    old_message = await remove_old_message(callback)
    await old_message.answer("Напишите вашу цель тренировок одним сообщением. На ответ есть 2 минуты.")
    start_action(
        bot=callback.bot,
        user_id=callback.from_user.id,
        kind="message",
        timeout=120,
        on_timeout=survey_message_timeout,
    )


@start_router.message(lambda message: message.from_user is not None and has_active_action(message.from_user.id))
async def survey_message(message: Message):
    action = get_active_action(message.from_user.id)
    if action is None or action.kind != "message":
        await message.answer("Сейчас ожидается другое действие.")
        return

    finish_action(message.from_user.id)
    await message.answer("Спасибо, ответ сохранён. Логика анкеты будет добавлена позже.")


async def survey_button_timeout(bot, user_id: int):
    await bot.send_message(user_id, "Время нажатия кнопки истекло. Нажмите «Подобрать формат занятий» ещё раз.")


async def survey_message_timeout(bot, user_id: int):
    await bot.send_message(user_id, "Время ожидания ответа истекло. Начните анкету заново, когда будете готовы.")
