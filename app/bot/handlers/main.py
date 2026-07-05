from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.cache import attachments_cache
from app.config import get_settings
from app.utils.message_resolver import remove_old_message

main_router = Router(name="start")

settings = get_settings()

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

async def check_subscription(message: types.Message, user_id: int) -> bool:
    subscriber = await message.bot.get_chat_member(chat_id=settings.telegram_channel_subscribe,
                                                   user_id=user_id)

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="📢 Подписаться", url=f"https://t.me/{settings.telegram_channel_subscribe[1:]}")
    keyboard.button(text="✅ Проверить подписку", callback_data="start:check_subscription")
    keyboard.adjust(1)

    if not subscriber or subscriber.status in ['kicked', 'left']:
        await message.answer(
            "📢 Подпишитесь сперва на канал Ильи!\n\n"
            "Здесь публикуются полезные материалы о тренировках, питании, восстановлении, разборы упражнений, "
            "результаты учеников и советы, которые помогут достичь цели без лишней воды.\n\n"
            "После подписки нажмите «✅ Проверить подписку».",
            reply_markup=keyboard.as_markup()
        )
        return False

    return True

@main_router.message(CommandStart())
async def start_command(message: types.Message) -> None:
    if not await check_subscription(message, message.from_user.id):
        return

    await message.answer_photo(
        photo=attachments_cache.get("app/attachments/main_menu.jpg"),
        caption=MAIN_MESSAGE,
        reply_markup=MAIN_BUTTONS.as_markup(),
    )

@main_router.callback_query(F.data == "start:check_subscription")
async def start_check_subscription(callback: CallbackQuery) -> None:
    await callback.answer()
    old_message = await remove_old_message(callback)

    if not await check_subscription(callback.message, callback.from_user.id):
        return

    await old_message.answer_photo(
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
