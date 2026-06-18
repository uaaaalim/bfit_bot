from dataclasses import dataclass

from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from groq import AsyncGroq

from app.bot.states.survey import SurveyState
from app.config import get_settings


@dataclass(frozen=True)
class SurveyQuestion:
    key: str
    title: str
    text: str
    timeout_seconds: int = 180
    min_length: int = 5
    max_length: int = 500


GROQ_CLIENT = AsyncGroq(api_key=get_settings().groq_api_key)

AI_PROMPT = """
You are a text extraction engine.

Task: analyze a user's free-form message and distribute their answers into the questionnaire below.

Rules:

1. Extract ONLY information explicitly written by the user.
2. Do NOT invent, guess or assume anything.
3. Do NOT rewrite text.
4. Do NOT summarize.
5. Keep user's wording exactly as written.
6. If there is no answer for a specific question, write exactly: Нет ответа.
7. One phrase can be used in multiple fields if relevant.
8. Return ONLY in Russian.
9. No comments, no explanations, no advice.

Format answers by sections.

--------------------------------

Блок 1: О вас

ФИО:
Дата рождения:
Способ связи:
Рост:
Вес:
Чем занимаетесь:
Активность работы:

Блок 2: Здоровье

Заболевания:
Лекарства:
Травмы:
Операции:
Аллергии:

Блок 3: Цели

Желаемый результат:
Цель по срокам:
Что нравится в тренировках:
Что не нравится в тренировках:

Блок 4: Текущая активность

Занимаетесь сейчас:
Частота тренировок:
Какие тренировки:
Длительность тренировки:
Опыт тренировок в зале:
Опыт работы с тренером:

Блок 5: Образ жизни

Питание:
Ограничения в питании:
Количество воды:
Количество сна:
Качество сна:
Уровень стресса:

Блок 6: Привычки

Курение:
Алкоголь:
Другие привычки:

Блок 7: Мотивация

Главный мотив:
Что мешало раньше:
Как комфортнее получать поддержку:

--------------------------------

Return EXACTLY in this format:

Блок 1: О вас
ФИО: ...
Дата рождения: ...
Способ связи: ...
Рост: ...
Вес: ...
Чем занимаетесь: ...
Активность работы: ...

Блок 2: Здоровье
Заболевания: ...
Лекарства: ...
Травмы: ...
Операции: ...
Аллергии: ...

Блок 3: Цели
Желаемый результат: ...
Цель по срокам: ...
Что нравится в тренировках: ...
Что не нравится в тренировках: ...

Блок 4: Текущая активность
Занимаетесь сейчас: ...
Частота тренировок: ...
Какие тренировки: ...
Длительность тренировки: ...
Опыт тренировок в зале: ...
Опыт работы с тренером: ...

Блок 5: Образ жизни
Питание: ...
Ограничения в питании: ...
Количество воды: ...
Количество сна: ...
Качество сна: ...
Уровень стресса: ...

Блок 6: Привычки
Курение: ...
Алкоголь: ...
Другие привычки: ...

Блок 7: Мотивация
Главный мотив: ...
Что мешало раньше: ...
Как комфортнее получать поддержку: ...

If missing → Нет ответа.
"""

SURVEY_QUESTIONS = [
    SurveyQuestion(
        key="main_information",
        title="Вопрос 1. Знакомство",
        text=(
            "Как вас зовут? Ваш возраст, рост, вес.\n"
            "Чем вы занимаетесь и насколько активна ваша работа "
            "(сидячая / подвижная)?"
        ),
        timeout_seconds=180,
        min_length=10,
        max_length=500,
    ),
    SurveyQuestion(
        key="health",
        title="Вопрос 2. Здоровье",
        text=(
            "Есть ли у вас заболевания или особенности здоровья, которые важно учитывать на тренировках?\n"
            "Принимаете ли вы сейчас какие-либо лекарства?\n"
            "Были ли травмы или операции, которые могут влиять на тренировки?\n"
            "Есть ли у вас аллергии?"
        ),
        timeout_seconds=180,
        min_length=3,
        max_length=700,
    ),
    SurveyQuestion(
        key="goals",
        title="Вопрос 3. Цели",
        text=(
            "Какой результат вы хотите получить от тренировок?\n"
            "Есть ли конкретная цель по срокам: событие, дата, форма?\n"
            "Что вам нравится в тренировках, а что — не очень?"
        ),
        timeout_seconds=180,
        min_length=10,
        max_length=700,
    ),
    SurveyQuestion(
        key="current_activity",
        title="Вопрос 4. Текущая активность",
        text=(
            "Занимаетесь ли вы сейчас? Если да — как часто?\n"
            "Какие тренировки или активности вы обычно делаете и сколько по времени?\n"
            "Есть ли опыт тренировок в зале или с тренером?"
        ),
        timeout_seconds=180,
        min_length=5,
        max_length=700,
    ),
    SurveyQuestion(
        key="lifestyle",
        title="Вопрос 5. Образ жизни",
        text=(
            "Как вы оцениваете своё питание?\n"
            "Есть ли ограничения или особенности в питании?\n"
            "Сколько воды вы примерно пьёте в день?\n"
            "Сколько часов вы спите и насколько хорошо высыпаетесь?\n"
            "Часто ли вы испытываете стресс?"
        ),
        timeout_seconds=180,
        min_length=5,
        max_length=800,
    ),
    SurveyQuestion(
        key="habits",
        title="Вопрос 6. Привычки",
        text=(
            "Курите ли вы?\n"
            "Употребляете ли алкоголь? Как часто?\n"
            "Есть ли ещё привычки, которые могут влиять на ваше здоровье или форму?"
        ),
        timeout_seconds=180,
        min_length=3,
        max_length=600,
    ),
    SurveyQuestion(
        key="motivation",
        title="Вопрос 7. Мотивация",
        text=(
            "Что для вас главный мотив начать тренировки?\n"
            "Что мешало вам заниматься регулярно раньше?\n"
            "Как вам комфортнее получать поддержку и обратную связь от тренера?"
        ),
        timeout_seconds=180,
        min_length=5,
        max_length=700,
    ),
]

async def send_question(message: Message, state: FSMContext, index: int) -> None:
    question = SURVEY_QUESTIONS[index]

    await state.update_data(current_question_index=index)
    await state.set_state(SurveyState.answering)

    await message.answer(
        text=(
            f"{question.title}\n\n"
            f"{question.text}\n\n"
            f"Ответьте текстовым сообщением. "
            f"На ответ выделено {question.timeout_seconds // 60} мин."
        )
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

async def finish_survey(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    await state.clear()

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🏠 Главное меню", callback_data="main_menu")
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
        temperature=0.1,
        max_completion_tokens=1000,
        top_p=1,
        reasoning_effort="low",
        stream=False,
        stop=None
    )

    author_id = get_settings().survey_receiver_id

    if not message.from_user.username:
        user = f'<a href="tg://user?id={message.from_user.id}">{message.from_user.full_name}</a>'
    else:
        user = f'@{message.from_user.username} ({message.from_user.full_name})'

    await message.bot.send_message(
        chat_id=author_id,
        text=(
            "🔥 Новый ответ на анкету в боте!\n\n"
            f"{completion.choices[0].message.content}\n\n"
            f"➡️ Перейти к контакту: {user}"
        )
    )
