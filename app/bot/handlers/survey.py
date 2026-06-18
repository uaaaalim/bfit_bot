from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.cache import attachments_cache, timeout_manager
from app.bot.services.survey import SURVEY_QUESTIONS, validate_answer, send_question, finish_survey
from app.bot.states.survey import SurveyState
from app.db.repositories import users_repo
from app.utils.message_resolver import remove_old_message

survey_router = Router(name="survey")

@survey_router.callback_query(F.data == "survey")
async def survey(callback: CallbackQuery, db_session: AsyncSession) -> None:
    user = await users_repo.get_by_telegram_id(db_session, telegram_id=callback.from_user.id)

    if user.passed_survey:
        await callback.answer()
        await callback.message.answer(text="🏋️ Вы уже заполнили анкету, во второй раз не получится :(")
        return

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="✅ Продолжить", callback_data="survey:continue")
    keyboard.button(text="🏠 На главный экран", callback_data="main_menu")
    keyboard.adjust(1)

    await callback.answer()
    old_message = await remove_old_message(callback)
    await old_message.answer_photo(
        photo=attachments_cache.get("app/attachments/survey/IMG_7790.JPG"),
        caption=(
            "Заполнение анкеты\n\n"
            "Ответьте на несколько вопросов. Отвечайте честно и понятно, это поможет в будущем "
            "подобрать под вас план тренировок и питания.\n\n"
            "Илья получит ваш контакт, далее он сможет связаться с вами и предложить подходящий вариант работы.\n\n"
            "Выберите опцию ниже чтобы продолжить"
        ),
        reply_markup=keyboard.as_markup()
    )

@survey_router.callback_query(F.data == "survey:continue")
async def survey_start(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()

    await callback.answer()
    old_message = await remove_old_message(callback)
    await old_message.answer(
        text=(
            "Приступим к анкете.\n\n"
            "Читайте вопросы внимательно и отвечайте как есть. "
            "Ответы помогут Илье лучше понять вашу ситуацию и подготовиться к разговору."
        )
    )
    await send_question(old_message, state, index=0)

@survey_router.message(SurveyState.answering)
async def process_survey_answer(message: Message, state: FSMContext, db_session: AsyncSession) -> None:
    timeout_manager.cancel(message.from_user.id)

    data = await state.get_data()
    index = data.get("current_question_index", 0)

    question = SURVEY_QUESTIONS[index]

    error = validate_answer(
        text=message.text,
        min_length=question.min_length,
        max_length=question.max_length,
    )

    user_id = message.from_user.id
    chat_id = message.chat.id
    bot = message.bot

    async def on_timeout() -> None:
        current_state = await state.get_state()
        current_data = await state.get_data()

        if (
                current_state == SurveyState.answering.state
                and current_data.get("current_question_index") == index
        ):
            await state.clear()

            keyboard = InlineKeyboardBuilder()
            keyboard.button(text="🔄️ Начать снова", callback_data="survey")
            keyboard.button(text="🏠 Главное меню", callback_data="main_menu")
            keyboard.adjust(1)

            await bot.send_message(
                chat_id=chat_id,
                text=(
                    "⏳ Время ожидания ответа вышло.\n\n"
                    "Анкета отменена. Вы можете начать заново через главное меню."
                ),
                reply_markup=keyboard.as_markup()
            )

    if error:
        await message.answer(error)
        timeout_manager.start(
            user_id=user_id,
            timeout_seconds=question.timeout_seconds,
            callback=on_timeout,
        )
        return

    answer = message.text.strip()

    await state.update_data(**{question.key: answer})
    next_index = index + 1

    if next_index >= len(SURVEY_QUESTIONS):
        await finish_survey(message, state, db_session)
        return

    await send_question(message, state, next_index)

    timeout_manager.start(
        user_id=user_id,
        timeout_seconds=question.timeout_seconds,
        callback=on_timeout,
    )
