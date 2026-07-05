import asyncio
import logging
from dataclasses import dataclass

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, User
from aiogram.utils.keyboard import InlineKeyboardBuilder
from groq import AsyncGroq
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.states.survey import SurveyState
from app.config import get_settings
from app.db.repositories import surveys_repo, users_repo


@dataclass(frozen=True)
class SurveyQuestion:
    key: str
    title: str
    text: str
    timeout_seconds: int = 180
    min_length: int = 5
    max_length: int = 500
    buttons: dict[str, str] = None

logger = logging.getLogger(__name__)
settings = get_settings()

GROQ_CLIENT = AsyncGroq(api_key=settings.groq_api_key)

AI_PROMPT = """
You are a data extraction engine.

Your task is to analyze the user's free-form text and extract only the information that directly answers the questionnaire fields below.

Rules:

1. Extract only information explicitly written by the user.
2. Do not invent, guess, infer, or assume anything.
3. Do not rewrite, paraphrase, summarize, or shorten the user's wording.
4. Keep the user's wording exactly as written.
5. If a field has no answer, write exactly: Нет ответа.
6. The same user phrase may be used in multiple fields if relevant.
7. Return the final answer only in Russian.
8. Do not add comments, explanations, advice, or extra text.
9. Follow the output format exactly.

Output format:

Блок 1: Личная информация
ФИО: ...
Дата рождения: ...
Рост: ...
Вес: ...
Профессия и уровень физической активности на работе: ...

Блок 2: Медицинская история
Хронические заболевания / состояния: ...
Регулярно принимаемые лекарства: ...
Травмы / операции: ...
Аллергии: ...

Блок 3: Фитнес-цели
Цели в фитнесе: ...
Даты / события для подготовки: ...
Что нравится в спорте / упражнениях: ...
Что не нравится в спорте / упражнениях: ...

Блок 4: Текущий уровень активности
Частота физической активности: ...
Виды активности и длительность: ...
Опыт с тренажерами / в спортзале: ...

Блок 5: Питание и образ жизни
Пищевые привычки: ...
Диетические ограничения / предпочтения: ...
Количество воды в день: ...
Количество сна: ...
Качество сна: ...
Частота стресса: ...

Блок 6: Вредные привычки
Курение: ...
Алкоголь: ...
Другие вредные привычки: ...

Блок 7: Мотивация и препятствия
Мотивация заниматься фитнесом: ...
Препятствия для регулярных тренировок: ...
Формат обратной связи и поддержки: ...

Блок 8:
Формат занятий: ...
Место проведения тренировок: ...
График тренировок: ...
"""

SURVEY_QUESTIONS = [
    SurveyQuestion(
        key="main_information",
        title="Блок 1. Знакомство",
        text=(
            "1. Ваш возраст\n"
            "2. Ваш рост и вес\n"
            "3. Профессия и уровень физической активности на работе?"
        ),
        timeout_seconds=180,
        min_length=10,
        max_length=500,
    ),
    SurveyQuestion(
        key="health",
        title="Блок 2. Медицинская история",
        text=(
            "1. Есть ли у вас хронические заболевания или состояния, которые могут повлиять на тренировки "
            "(сердечно-сосудистые, диабет, артрит и т.д.)?\n"
            "2. Принимаете ли вы какие-либо лекарства на регулярной основе?\n"
            "3. Были ли травмы, которые могут повлиять на физическую активность (переломы, растяжения, операции)?\n"
            "4. Есть ли аллергии, о которых мне следует знать?"
        ),
        timeout_seconds=180,
        min_length=3,
        max_length=700,
    ),
    SurveyQuestion(
        key="goals",
        title="Блок 3: Фитнес-цели",
        text=(
            "1. Какие у вас цели в фитнесе? (Похудение, набор массы, улучшение выносливости, реабилитация и т.д.)\n"
            "2. Есть ли конкретные даты или события, к которым вы хотите подготовиться?\n"
            "3. Какие виды спорта или упражнения вам нравятся/не нравятся?"
        ),
        timeout_seconds=180,
        min_length=10,
        max_length=700,
    ),
    SurveyQuestion(
        key="current_activity",
        title="Блок 4. Текущий уровень активности",
        text=(
            "1. Как часто вы сейчас занимаетесь физической активностью?\n"
            "2. Какие виды активности и как долго вы обычно выполняете?\n"
            "3. Есть ли у вас опыт работы с тренажерами или в спортзале?"
        ),
        timeout_seconds=180,
        min_length=5,
        max_length=700,
    ),
    SurveyQuestion(
        key="lifestyle",
        title="Блок 5. Питание и образ жизни",
        text=(
            "1. Как вы оцениваете свои пищевые привычки?\n"
            "2. Есть ли у вас какие-либо диетические ограничения или предпочтения?\n"
            "3. Сколько в среднем литров воды вы пьете в день?\n"
            "4. Сколько часов в среднем вы спите ночью? Как вы оцениваете качество вашего сна?\n"
            "5. Как часто вы испытываете стресс?"
        ),
        timeout_seconds=180,
        min_length=5,
        max_length=800,
    ),
    SurveyQuestion(
        key="habits",
        title="Блок 6. Вредные привычки",
        text=(
            "1. Курите ли вы? Если да, то как часто?\n"
            "2. Употребляете ли вы алкоголь? Если да, то как часто и в каких количествах?\n"
            "3. Есть ли другие вредные привычки, которые могут повлиять на вашу физическую активность "
            "или здоровье в целом?"
        ),
        timeout_seconds=180,
        min_length=3,
        max_length=600,
    ),
    SurveyQuestion(
        key="motivation",
        title="Блок 7. Мотивация и препятствия",
        text=(
            "1. Что мотивирует вас заниматься фитнесом?\n"
            "2. Какие основные препятствия мешали вам ранее поддерживать регулярные тренировки?\n"
            "3. Как вы предпочитаете получать обратную связь и поддержку во время тренировочного процесса?"
        ),
        timeout_seconds=180,
        min_length=5,
        max_length=700,
    ),
    SurveyQuestion(
        key="format_of_trains",
        title="Блок 8. Формат занятий",
        text=(
            "Очные тренировки веду только в БЦ «Аврора». Если не подходит локация — можно выбрать онлайн-формат.\n"
            "Как вы предпочитаете проводить тренировки?"
        ),
        timeout_seconds=60,
        buttons={
            "survey:8:1:online": "🟢 Онлайн",
            "survey:8:1:aurora": "🏢 В БЦ Аврора",
        }
    ),
    SurveyQuestion(
        key="trains_schedule",
        title="Блок 8. График тренировок",
        text=(
            "Сколько раз в неделю планируете тренироваться?"
        ),
        timeout_seconds=60,
        buttons={
            "survey:8:3:1": "🔘 Вторник / Четверг",
            "survey:8:3:2": "🔘 Вторник / Четверг / Суббота",
            "survey:8:3:3": "🔘 Понедельник / Среда / Пятница",
            "survey:8:3:4": "🔘 Другое: обсудим лично",
        },
    ),
    SurveyQuestion(
        key="trains_format",
        title="Блок 8. Время проведения тренировок",
        text=(
            "В какое время вам удобнее тренироваться?"
        ),
        timeout_seconds=60,
        buttons={
            "survey:8:2:day": "☀️ Днем (13:00 - 16:00)",
            "survey:8:2:evening": "🌃 Вечером (16:00 - 21:00)"
        },
    ),
]

async def send_question(message: Message, state: FSMContext, index: int) -> None:
    question = SURVEY_QUESTIONS[index]

    await state.update_data(current_question_index=index)
    await state.set_state(SurveyState.answering)

    reply_markup = None

    if question.buttons:
        keyboard = InlineKeyboardBuilder()

        for callback_data, button_text in question.buttons.items():
            keyboard.button(text=button_text, callback_data=callback_data)

        keyboard.adjust(1)
        reply_markup = keyboard.as_markup()

        attention = "Выберите один из вариантов ниже"
    else:
        attention = "Ответьте текстовым сообщением"

    await message.answer(
        text=(
            f"{question.title}\n\n"
            f"{question.text}\n\n"
            f"{attention}. На ответ выделено {question.timeout_seconds // 60} мин."
        ),
        reply_markup=reply_markup
    )

def validate_answer(
        text: str | None,
        min_length: int,
        max_length: int
) -> str | None:
    if not text:
        return "❌ Ошибка ввода: ответ должен быть текстом."

    clean_text = text.strip()

    if len(clean_text) > max_length:
        return f"❌ Ответ слишком длинный. Максимум: {max_length} символов."

    if len(clean_text) < min_length:
        return "🏋️ Напишите чуть подробнее, чтобы Илья получил полезную информацию."

    return None

async def analyze_survey(data: dict) -> str | None:
    max_attempts = 3

    for attempt in range(max_attempts):
        try:
            completion = await GROQ_CLIENT.chat.completions.create( # type: ignore
                model="openai/gpt-oss-20b",
                messages=[
                    {
                        "role": "system",
                        "content": AI_PROMPT
                    },
                    {
                        "role": "user",
                        "content": str(data)
                    }
                ],
                temperature=0.3,
                max_completion_tokens=1000,
                top_p=1,
                reasoning_effort="low",
                stream=False
            )

            content = completion.choices[0].message.content

            if not content:
                raise ValueError("Empty AI response")
            elif not all(f"Блок {block + 1}" in content for block in range(8)):
                raise ValueError("Malformed AI response")

            return content

        except Exception as e:
            logger.warning(
                "AI analyze failed attempt %s: %s",
                attempt + 1,
                e
            )

            if attempt < max_attempts - 1:
                await asyncio.sleep(2)

    return None

def format_raw_survey(data: dict) -> str:
    return (
        "⚠️ ИИ-анализ недоступен. Отправлены исходные ответы.\n\n"
        f"Знакомство:\n{data.get('main_information', 'Нет ответа')}\n\n"
        f"Здоровье:\n{data.get('health', 'Нет ответа')}\n\n"
        f"Цели:\n{data.get('goals', 'Нет ответа')}\n\n"
        f"Текущая активность:\n{data.get('current_activity', 'Нет ответа')}\n\n"
        f"Образ жизни:\n{data.get('lifestyle', 'Нет ответа')}\n\n"
        f"Привычки:\n{data.get('habits', 'Нет ответа')}\n\n"
        f"Мотивация:\n{data.get('motivation', 'Нет ответа')}"
    )

async def finish_survey(message: Message, state: FSMContext, db_session: AsyncSession, survey_user: User) -> None:
    data = await state.get_data()
    await state.clear()

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🏠 Главное меню", callback_data="main_menu")
    keyboard.button(url="https://t.me/bfit360", text="🏋️ Fitness 360 - Телеграм Канал Ильи")
    keyboard.button(url="https://t.me/ilyamunfit", text="Связаться в Telegram")
    keyboard.button(url="https://instagram.com/ilyamun.fit", text="Страничка в Instagram")
    keyboard.button(url="https://tiktok.com/@ilyamunfit2", text="Я в TikTok")
    keyboard.adjust(1)

    await message.answer(
        text=(
            "📃 Спасибо за заполнение анкеты. Илья уже ее получил и ознакомится с ней при первой же возможности.\n\n"
            "Ваши контакты были переданы ему, и он с Вами вскоре свяжется!"
        ),
        reply_markup=keyboard.as_markup()
    )

    user = await users_repo.get_by_telegram_id(db_session, telegram_id=survey_user.id)
    if not user:
        return

    name = "Не указано"
    if user.name:
        name = user.name
    data['full_name'] = name

    analysis = await analyze_survey(data)

    if analysis is None:
        analysis = format_raw_survey(data)

    author_id = get_settings().survey_receiver_id

    if not survey_user.username:
        user_link = f'<a href="tg://user?id={survey_user.id}">{survey_user.full_name}</a>'
    else:
        user_link = f'@{survey_user.username} ({survey_user.full_name})'

    await surveys_repo.set_data(
        db_session,
        telegram_id=survey_user.id,
        raw_data=str(data),
        detailed_data=analysis,
    )
    await message.bot.send_message(
        chat_id=author_id,
        text=(
            "🔥 Новый ответ на анкету в боте!\n\n"
            f"{analysis}\n\n"
            f"➡️ Перейти к контакту: {user_link}"
        )
    )
