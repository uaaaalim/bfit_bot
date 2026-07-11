from aiogram import Router, types, F, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.cache import attachments_cache, timeout_manager
from app.bot.states.acquaintance import AcquaintanceState
from app.config import get_settings
from app.db.repositories import users_repo
from app.utils.message_resolver import remove_old_message

main_router = Router(name="start")

settings = get_settings()

MAIN_MESSAGE = (
    "Это бот Ильи, персонального тренера 🏋️ Здесь можно посмотреть результаты учеников, узнать об Илье "
    "и оставить заявку на подбор формата занятий.\n\n"
    "Хотите начать тренировки, вернуться в форму или понять, какой формат вам подойдёт? "
    "Заполните короткую анкету — Илья посмотрит вашу цель, опыт и возможные ограничения, "
    "после чего свяжется с вами лично."
)

MAIN_BUTTONS = InlineKeyboardBuilder()
MAIN_BUTTONS.button(text="🎯 Подобрать формат занятий", callback_data="survey")
MAIN_BUTTONS.button(text="📸 Примеры работы", callback_data="main_menu:results:1")
MAIN_BUTTONS.button(text="🏆 Кто такой Илья", callback_data="about")
MAIN_BUTTONS.button(
    text="👥 Получать полезные материалы",
    url=f"https://t.me/{settings.telegram_channel_subscribe[1:]}"
)
MAIN_BUTTONS.adjust(1, 2, 1)


def schedule_acquaintance_timeout(user_id: int, bot: Bot, chat_id: int, state: FSMContext) -> None:
    async def on_timeout() -> None:
        current_state = await state.get_state()

        if current_state != AcquaintanceState.answering.state:
            return

        await state.clear()

        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="👋 Попробовать заново", callback_data="start:acquaintance")
        keyboard.adjust(1)

        await bot.send_message(
            chat_id=chat_id,
            text=(
                "⏳ Время ожидания ответа вышло.\n\n"
                "Вы можете попробовать, нажав на кнопку ниже"
            ),
            reply_markup=keyboard.as_markup(),
        )

    timeout_manager.start(
        user_id=user_id,
        timeout_seconds=120,
        callback=on_timeout,
    )


async def check_user_name(message: types.Message, user_id: int, db_session: AsyncSession, state: FSMContext) -> bool:
    user = await users_repo.get_by_telegram_id(session=db_session, telegram_id=user_id)

    if not user.name:
        await state.clear()
        timeout_manager.cancel(user_id)

        await message.answer(
            "👋 Перед началом давайте познакомимся.\n\n"
            "Как к вам можно обращаться? Введите, пожалуйста, ваше имя в сообщении"
        )

        await state.set_state(AcquaintanceState.answering)
        schedule_acquaintance_timeout(
            user_id=user_id,
            chat_id=message.chat.id,
            bot=message.bot,
            state=state
        )

        return False

    return True


@main_router.message(CommandStart())
async def start_command(message: types.Message, db_session: AsyncSession, state: FSMContext) -> None:
    if not await check_user_name(message, message.from_user.id, db_session, state):
        return

    await message.answer_photo(
        photo=attachments_cache.get("app/attachments/main_menu.jpg"),
        caption=MAIN_MESSAGE,
        reply_markup=MAIN_BUTTONS.as_markup(),
    )


@main_router.callback_query(F.data == "start:acquaintance")
async def acquaintance_button(callback: CallbackQuery, db_session: AsyncSession, state: FSMContext) -> None:
    await callback.answer()
    old_message = await remove_old_message(callback)

    if not await check_user_name(callback.message, callback.from_user.id, db_session, state):
        return

    await old_message.answer_photo(
        photo=attachments_cache.get("app/attachments/main_menu.jpg"),
        caption=MAIN_MESSAGE,
        reply_markup=MAIN_BUTTONS.as_markup(),
    )


@main_router.message(AcquaintanceState.answering)
async def acquaintance_message(message: types.Message, db_session: AsyncSession, state: FSMContext) -> None:
    timeout_manager.cancel(message.from_user.id)

    if not message.text:
        await message.answer("Напишите имя текстом 🙂")

        schedule_acquaintance_timeout(
            user_id=message.from_user.id,
            chat_id=message.chat.id,
            bot=message.bot,
            state=state
        )

        return

    name = message.text.strip()

    if len(name) < 2 or len(name) > 50:
        await message.answer("Введите имя чуть понятнее 🙂")

        schedule_acquaintance_timeout(
            user_id=message.from_user.id,
            chat_id=message.chat.id,
            bot=message.bot,
            state=state
        )

        return

    await users_repo.set_name(session=db_session, telegram_id=message.from_user.id, value=name)
    await state.clear()

    await message.answer_photo(
        photo=attachments_cache.get("app/attachments/main_menu.jpg"),
        caption=MAIN_MESSAGE,
        reply_markup=MAIN_BUTTONS.as_markup(),
    )


@main_router.callback_query(F.data == "main_menu")
async def main_menu_button(callback: CallbackQuery) -> None:
    await callback.answer()
    old_message = await remove_old_message(callback)
    await old_message.answer_photo(
        photo=attachments_cache.get("app/attachments/main_menu.jpg"),
        caption=MAIN_MESSAGE,
        reply_markup=MAIN_BUTTONS.as_markup(),
    )
