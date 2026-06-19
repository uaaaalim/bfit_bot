# BFIT Bot 🏋️‍♂️

**BFIT Bot** — Telegram-бот для персонального тренера Ильи: показывает информацию о тренере, результаты учеников, контакты и собирает анкету для подбора формата занятий. После прохождения анкеты бот анализирует ответы через Groq API, отправляет структурированный результат тренеру и отмечает пользователя в базе, чтобы анкету нельзя было заполнить повторно.

## Что умеет проект

- 🚀 Работает на **aiogram 3** и асинхронном polling.
- 🧠 Использует **FSM** для пошаговой анкеты пользователя.
- ⏳ Поддерживает таймеры ожидания ответа: если пользователь не ответил вовремя, анкета отменяется.
- 🗄️ Хранит пользователей и кэш Telegram `file_id` вложений в **PostgreSQL**.
- 🔁 Управляет схемой БД через **Alembic**.
- 🤖 Анализирует свободные ответы анкеты через **Groq API**.
- 🧩 Разделён на роутеры, хендлеры, middleware, сервисы, модели и репозитории.
- 📝 Имеет настраиваемое логирование в консоль и файл.

---

## Стек

- **Python** `>=3.14,<3.15`
- **aiogram** `>=3.29.0,<4.0.0`
- **SQLAlchemy asyncio** `>=2.0.51,<3.0.0`
- **asyncpg** `>=0.31.0,<0.32.0`
- **Alembic** `>=1.18.4,<2.0.0`
- **Pydantic / pydantic-settings**
- **python-dotenv**
- **Groq SDK**
- **Poetry** для зависимостей и виртуального окружения

---

## Структура проекта

```text
app/
├── bot/
│   ├── cache/          # кэш вложений и менеджер таймеров
│   ├── filters/        # кастомные фильтры
│   ├── handlers/       # обработчики команд, callback и сообщений
│   ├── middlewares/    # middleware БД и пользователей
│   ├── services/       # бизнес-логика, например анкета
│   ├── states/         # FSM-состояния
│   ├── routers.py      # список подключаемых роутеров
│   └── setup.py        # создание Bot и Dispatcher
├── db/
│   ├── models/         # SQLAlchemy-модели
│   ├── repositories/   # функции доступа к БД
│   ├── base.py         # Base и TimestampMixin
│   └── session.py      # engine/session_factory/get_session
├── config.py           # настройки из .env
├── logger.py           # настройка логирования
└── main.py             # точка запуска приложения

alembic/                # миграции
run.py                  # запуск бота
.env.example            # пример переменных окружения
pyproject.toml          # зависимости Poetry
```

---

## Настройка `.env`

Скопируйте пример окружения:

```bash
cp .env.example .env
```

Для Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Заполните `.env` по примеру:

```env
BOT_TOKEN=1234567890:telegram_bot_token

POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=bfit_bot

ADMIN_IDS=111111111,222222222
MEDIA_CHECK_VICTIM_ID=111111111
SURVEY_RECEIVER_ID=111111111

GROQ_API_KEY=gsk_your_groq_key
```

### Что означают переменные

| Переменная | Описание |
| --- | --- |
| `BOT_TOKEN` | Токен Telegram-бота из [@BotFather](https://t.me/BotFather). |
| `POSTGRES_HOST` | Хост PostgreSQL. Для локального запуска обычно `localhost`. |
| `POSTGRES_PORT` | Порт PostgreSQL, обычно `5432`. |
| `POSTGRES_USER` | Пользователь PostgreSQL. |
| `POSTGRES_PASSWORD` | Пароль пользователя PostgreSQL. |
| `POSTGRES_DB` | Название базы данных. |
| `ADMIN_IDS` | Telegram ID администраторов через запятую. Используется фильтром администратора. |
| `MEDIA_CHECK_VICTIM_ID` | Telegram ID чата/пользователя для проверки и кэширования медиафайлов. |
| `SURVEY_RECEIVER_ID` | Telegram ID получателя готовых анкет. |
| `GROQ_API_KEY` | API-ключ Groq для анализа ответов анкеты. |

Дополнительно в `app/config.py` есть настройки логирования с дефолтными значениями: `LOG_DIR`, `LOG_LEVEL`, `LOG_FILE_MAX_MB`, `LOG_FOLDER_MAX_MB`, `LOG_TO_CONSOLE`, `LOG_TO_FILE`.

---

## Установка Poetry

### Ubuntu / Debian

Рекомендуемый способ установки Poetry:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Добавьте Poetry в `PATH`, если установщик попросил это сделать:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Проверьте установку:

```bash
poetry --version
```

### Windows PowerShell

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

Если команда `poetry` не находится, добавьте в `Path` папку:

```text
%APPDATA%\Python\Scripts
```

Проверка:

```powershell
poetry --version
```

---

## Установка зависимостей

Проект рассчитан на Python `>=3.14,<3.15`, поэтому сначала убедитесь, что нужная версия Python установлена:

```bash
python --version
```

Чтобы виртуальное окружение создавалось прямо внутри проекта в папке `.venv`, выполните:

```bash
poetry config virtualenvs.in-project true
```

Выберите интерпретатор и установите зависимости:

```bash
poetry env use python3.14
poetry install
```

На Windows команда может выглядеть так:

```powershell
poetry env use 3.14
poetry install
```

Проверка окружения:

```bash
poetry run python --version
```

---

## Как устроены хендлеры

Хендлеры лежат в `app/bot/handlers/`. Каждый файл создаёт свой `Router`, регистрирует обработчики и экспортирует роутер. Затем роутер нужно добавить в список `ROUTERS` в `app/bot/routers.py`.

### Пример команды `/start`

```python
from aiogram import Router, types
from aiogram.filters import CommandStart

main_router = Router(name="start")

@main_router.message(CommandStart())
async def start_command(message: types.Message) -> None:
    await message.answer("Привет! Это главное меню.")
```

### Пример callback-хендлера кнопки

```python
from aiogram import F, Router
from aiogram.types import CallbackQuery

example_router = Router(name="example")

@example_router.callback_query(F.data == "example:open")
async def open_example(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.answer("Кнопка нажата ✅")
```

### Подключение нового роутера

```python
from app.bot.handlers.example import example_router

ROUTERS = [
    main_router,
    example_router,
]
```

---

## Кнопки и сообщения

В проекте используются `InlineKeyboardBuilder` и callback data.

### Создать inline-кнопки

```python
from aiogram.utils.keyboard import InlineKeyboardBuilder

keyboard = InlineKeyboardBuilder()
keyboard.button(text="🏠 Главное меню", callback_data="main_menu")
keyboard.button(text="📸 Примеры работы", callback_data="main_menu:results:1")
keyboard.adjust(1)

await message.answer("Выберите действие:", reply_markup=keyboard.as_markup())
```

### Отправить сообщение с картинкой

```python
await message.answer_photo(
    photo=attachments_cache.get("app/attachments/main_menu.jpg"),
    caption="Текст под фото",
    reply_markup=keyboard.as_markup(),
)
```

`attachments_cache` нужен, чтобы брать уже сохранённый Telegram `file_id` и не загружать один и тот же файл каждый раз заново.

---

## FSM и таймеры

FSM используется для анкеты в `app/bot/handlers/survey.py`, а состояния описаны в `app/bot/states/survey.py`.

### Минимальный пример состояния

```python
from aiogram.fsm.state import State, StatesGroup

class MyState(StatesGroup):
    waiting_text = State()
```

### Записать данные и перевести пользователя в состояние

```python
await state.update_data(current_question_index=0)
await state.set_state(MyState.waiting_text)
await message.answer("Напишите ответ текстом")
```

### Обработать сообщение в состоянии

```python
@router.message(MyState.waiting_text)
async def process_text(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    await state.clear()
    await message.answer(f"Готово, данные: {data}")
```

### Таймер ожидания

Для таймеров используется `TimeoutManager` из `app/bot/cache/timeouts.py`. Он создаёт `asyncio.Task`, ждёт нужное количество секунд и вызывает callback, если таймер не отменили.

Упрощённый пример:

```python
from app.bot.cache import timeout_manager

timeout_manager.start(
    user_id=message.from_user.id,
    timeout_seconds=180,
    callback=on_timeout,
)

# Когда пользователь ответил — отменяем старый таймер:
timeout_manager.cancel(message.from_user.id)
```

В анкете таймер запускается после каждого вопроса. Если пользователь отвечает корректно, старый таймер отменяется и создаётся новый для следующего вопроса.

---

## Работа с базой данных

Подключение к БД собирается из переменных `POSTGRES_*` в `app/config.py` и используется в `app/db/session.py`.

### Получить `AsyncSession` в хендлере

`DbSessionMiddleware` автоматически добавляет `db_session` в аргументы хендлера:

```python
from sqlalchemy.ext.asyncio import AsyncSession

@router.callback_query(F.data == "profile")
async def profile(callback: CallbackQuery, db_session: AsyncSession) -> None:
    ...
```

Middleware сам делает `commit()` после успешного хендлера и `rollback()` при ошибке.

### Создать модель

Модели лежат в `app/db/models/` и наследуются от `Base`. Если нужны `created_at` и `updated_at`, добавьте `TimestampMixin`.

```python
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin

class Workout(Base, TimestampMixin):
    __tablename__ = "workouts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
```

После создания модели добавьте её импорт в `app/db/models/__init__.py`, чтобы Alembic видел таблицу при автогенерации.

### Создать репозиторий

Репозитории в проекте — это обычные async-функции, которые принимают `AsyncSession` первым аргументом.

```python
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Workout

async def get_by_id(session: AsyncSession, workout_id: int) -> Workout | None:
    result = await session.execute(
        select(Workout).where(Workout.id == workout_id)
    )
    return result.scalar_one_or_none()
```

### Использовать репозиторий в хендлере

```python
from app.db.repositories import users_repo

@router.message(Command("me"))
async def me(message: Message, db_session: AsyncSession) -> None:
    user = await users_repo.get_by_telegram_id(
        db_session,
        telegram_id=message.from_user.id,
    )
    await message.answer(f"Ваш ID в Telegram: {user.telegram_id}")
```

---

## Миграции Alembic

Перед миграциями убедитесь, что PostgreSQL запущен, база создана, а `.env` заполнен.

### Применить миграции

```bash
poetry run alembic upgrade head
```

### Создать новую миграцию автоматически

```bash
poetry run alembic revision --autogenerate -m "add workouts table"
```

### Создать пустую миграцию вручную

```bash
poetry run alembic revision -m "custom migration"
```

### Откатить последнюю миграцию

```bash
poetry run alembic downgrade -1
```

После автогенерации обязательно откройте файл в `alembic/versions/` и проверьте, что Alembic создал именно те изменения, которые нужны.

---

## Запуск бота

1. Заполните `.env`.
2. Запустите PostgreSQL.
3. Примените миграции:

```bash
poetry run alembic upgrade head
```

4. Запустите бота:

```bash
poetry run python run.py
```

При запуске бот:

- настраивает логирование;
- создаёт `Bot` и `Dispatcher`;
- подключает middleware и роутеры;
- проверяет/кэширует медиафайлы;
- сбрасывает webhook и запускает polling.

---

## Полезные команды

```bash
# установить зависимости
poetry install

# запустить бота
poetry run python run.py

# применить миграции
poetry run alembic upgrade head

# создать миграцию по моделям
poetry run alembic revision --autogenerate -m "migration name"

# посмотреть текущую ревизию БД
poetry run alembic current
```

---

## Небольшие советы по разработке

- Один экран/раздел бота — один файл в `app/bot/handlers/` и отдельный `Router`.
- Callback data лучше делать предсказуемой: `section:action:id`, например `main_menu:results:1`.
- Не забывайте вызывать `await callback.answer()`, чтобы Telegram не показывал вечную загрузку на кнопке.
- Для долгих сценариев используйте FSM, а промежуточные данные храните в `FSMContext`.
- Любую работу с БД делайте через `db_session`, который приходит из middleware.
- После изменения моделей всегда создавайте и проверяйте миграцию.
- Секреты не коммитьте: реальные значения должны быть только в локальном `.env`.
