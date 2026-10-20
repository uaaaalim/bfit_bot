# BFIT Bot 🏋️‍♂️

**BFIT Bot** — Telegram-бот персонального тренера Ильи Муна. Бот знакомит пользователя с тренером, показывает квалификацию, подход к тренировкам, примеры результатов, контакты и собирает анкету для подбора формата занятий. Перед началом работы бот проверяет подписку на Telegram-канал, сохраняет имя пользователя, проводит пошаговую анкету и отправляет Илье структурированный результат.

## Возможности

- 🚀 Асинхронный Telegram-бот на **aiogram 3** в режиме polling.
- 📢 Проверка подписки на обязательный Telegram-канал перед показом главного меню.
- 👋 Первичное знакомство: бот запрашивает и сохраняет имя пользователя.
- 🧠 Пошаговая анкета на **FSM** с текстовыми ответами и inline-вариантами выбора.
- ⏳ Таймеры ожидания ответа для знакомства и каждого шага анкеты.
- 🤖 Анализ свободных ответов через **Groq API** с fallback на отправку исходных данных.
- 📬 Отправка готовой анкеты в отдельный Telegram-чат/пользователю из настроек.
- 🗄️ Хранение пользователей, результатов анкет и Telegram `file_id` медиафайлов в **PostgreSQL**.
- 🖼️ Автоматическая проверка, загрузка и кэширование изображений/видео при старте бота.
- 🔁 Управление схемой БД через **Alembic**.
- 🧩 Разделение кода на routers, handlers, middlewares, services, repositories и models.
- 📝 Настраиваемое логирование в консоль и файл.

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
- **Poetry** для управления зависимостями

---

## Структура проекта

```text
app/
├── attachments/              # локальные изображения, документы и видео для бота
├── bot/
│   ├── cache/                # in-memory cache file_id и менеджер timeout-задач
│   ├── filters/              # кастомные фильтры
│   ├── handlers/             # обработчики команд, callback и сообщений
│   ├── middlewares/          # middleware БД и автоматического создания пользователя
│   ├── services/             # бизнес-логика анкеты и AI-анализа
│   ├── states/               # FSM-состояния знакомства и анкеты
│   ├── attachments.py        # декларация и загрузка медиафайлов в Telegram
│   ├── routers.py            # список подключаемых роутеров
│   └── setup.py              # создание Bot и Dispatcher
├── db/
│   ├── models/               # SQLAlchemy-модели: users, attachments, surveys
│   ├── repositories/         # async-функции доступа к БД
│   ├── base.py               # Base и TimestampMixin
│   └── session.py            # engine, session_factory, get_session
├── utils/                    # вспомогательные функции
├── config.py                 # настройки из .env
├── logger.py                 # настройка логирования
└── main.py                   # основной сценарий запуска

alembic/                      # миграции БД
run.py                        # CLI-точка запуска бота
.env.example                  # пример переменных окружения
pyproject.toml                # зависимости Poetry
```

---

## Переменные окружения

Скопируйте пример окружения:

```bash
cp .env.example .env
```

Для Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Заполните `.env`:

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
TELEGRAM_CHANNEL_SUBSCRIBE=@bfit360

GROQ_API_KEY=gsk_your_groq_key
```

| Переменная | Описание |
| --- | --- |
| `BOT_TOKEN` | Токен Telegram-бота из [@BotFather](https://t.me/BotFather). |
| `POSTGRES_HOST` | Хост PostgreSQL. Для локального запуска обычно `localhost`. |
| `POSTGRES_PORT` | Порт PostgreSQL, обычно `5432`. |
| `POSTGRES_USER` | Пользователь PostgreSQL. |
| `POSTGRES_PASSWORD` | Пароль пользователя PostgreSQL. |
| `POSTGRES_DB` | Название базы данных. |
| `ADMIN_IDS` | Telegram ID администраторов через запятую. Сейчас используется как общая настройка для admin-фильтра. |
| `MEDIA_CHECK_VICTIM_ID` | Telegram ID чата/пользователя, куда бот отправляет новые медиа для получения и кэширования `file_id`. |
| `SURVEY_RECEIVER_ID` | Telegram ID получателя заполненных анкет. |
| `TELEGRAM_CHANNEL_SUBSCRIBE` | Обязательный канал для подписки, например `@bfit360`. Бот проверяет подписку через `get_chat_member`. |
| `GROQ_API_KEY` | API-ключ Groq для анализа ответов анкеты. |

Дополнительные настройки логирования имеют значения по умолчанию и при необходимости тоже могут быть заданы в `.env`: `LOG_DIR`, `LOG_LEVEL`, `LOG_FILE_MAX_MB`, `LOG_FOLDER_MAX_MB`, `LOG_TO_CONSOLE`, `LOG_TO_FILE`.

---

## Быстрый старт

1. Установите Python `>=3.14,<3.15` и Poetry.
2. Создайте `.env` и заполните переменные окружения.
3. Убедитесь, что PostgreSQL запущен и база данных создана.
4. Установите зависимости:

```bash
poetry config virtualenvs.in-project true
poetry env use python3.14
poetry install
```

5. Примените миграции:

```bash
poetry run alembic upgrade head
```

6. Запустите бота:

```bash
poetry run python run.py
```

При старте бот настраивает логирование, создаёт `Bot` и `Dispatcher`, подключает middleware и роутеры, проверяет/кэширует медиафайлы, удаляет webhook и запускает polling.

---

## Запуск через Docker Compose

Создайте `.env` из `.env.example` и заполните настройки бота, а также
`POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`. Для новой контейнерной БД
можно выбрать `POSTGRES_USER=bfit` и `POSTGRES_DB=bfit_bot`; пароль задайте свой.
Compose запускает отдельный PostgreSQL и автоматически задаёт боту
`POSTGRES_HOST=postgres` и `POSTGRES_PORT=5432`, переопределяя значения из `.env`.
Существующая внешняя база данных при этом не используется.

```bash
docker compose up -d --build
docker compose logs -f bfit-bot
```

Бот ждёт готовности PostgreSQL, применяет миграции Alembic и запускает polling.
При ошибке миграции запуск бота не выполняется. Логи идут в Docker с ротацией.
Данные PostgreSQL хранятся в именованном volume `postgres_data`.

После обновления кода повторите `docker compose up -d --build`.
Для остановки используйте `docker compose down`: данные БД сохранятся.
Команда `docker compose down -v` удаляет и данные БД.
Изменение `POSTGRES_USER`, `POSTGRES_PASSWORD` или `POSTGRES_DB` в `.env`
не меняет учётные данные уже инициализированной базы в volume.

---

## Установка Poetry

### Ubuntu / Debian

```bash
curl -sSL https://install.python-poetry.org | python3 -
export PATH="$HOME/.local/bin:$PATH"
poetry --version
```

### Windows PowerShell

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
poetry --version
```

Если команда `poetry` не находится, добавьте в `Path` папку:

```text
%APPDATA%\Python\Scripts
```

---

## Пользовательский сценарий

1. Пользователь отправляет `/start`.
2. Бот проверяет подписку на канал из `TELEGRAM_CHANNEL_SUBSCRIBE`.
3. Если подписки нет, бот показывает кнопки «Подписаться» и «Проверить подписку».
4. После подписки бот спрашивает имя, если оно ещё не сохранено в таблице `users`.
5. Пользователь попадает в главное меню:
   - 🎯 подобрать формат занятий;
   - 📸 посмотреть примеры работы;
   - 🏆 узнать, кто такой Илья.
6. При запуске анкеты бот не даёт заполнить её повторно, если для `telegram_id` уже есть запись в `surveys`.
7. Анкета проходит по блокам: личная информация, здоровье, цели, активность, образ жизни, привычки, мотивация, формат/место/график тренировок.
8. После завершения бот благодарит пользователя, анализирует ответы через Groq и отправляет Илье готовый результат с контактом пользователя.

---

## Медиафайлы и кэш `file_id`

Список используемых файлов объявлен в `app/bot/attachments.py` в константе `ATTACHMENTS`. При старте `check_attachments()`:

- получает ID текущего бота;
- загружает сохранённые `file_id` из таблицы `attachments`;
- удаляет из БД устаревшие записи, которых больше нет в `ATTACHMENTS`;
- отправляет новые локальные файлы в чат `MEDIA_CHECK_VICTIM_ID`;
- сохраняет полученные Telegram `file_id` в БД и in-memory cache.

Если добавляете новое изображение или видео для хендлера, положите файл в `app/attachments/`, добавьте его в `ATTACHMENTS`, затем используйте:

```python
from app.bot.cache import attachments_cache

file_id = attachments_cache.get("app/attachments/main_menu.jpg")
```

---

## Хендлеры и роутеры

Хендлеры лежат в `app/bot/handlers/`. Каждый файл создаёт свой `Router`, регистрирует обработчики и экспортирует роутер. Новый роутер нужно добавить в `ROUTERS` в `app/bot/routers.py`.

Основные разделы:

| Файл | Назначение |
| --- | --- |
| `main.py` | `/start`, проверка подписки, знакомство, главное меню. |
| `about.py` | Информация об Илье. |
| `qualifications.py` | Квалификация и документы. |
| `approach.py` | Подход к тренировкам и MTR-10. |
| `results.py` | Пагинация примеров работы с фото и видео. |
| `survey.py` | Запуск, прохождение и завершение анкеты. |
| `contacts.py` | Контакты и социальные сети. |

Пример callback-хендлера:

```python
from aiogram import F, Router
from aiogram.types import CallbackQuery

example_router = Router(name="example")

@example_router.callback_query(F.data == "example:open")
async def open_example(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.answer("Кнопка нажата ✅")
```

---

## FSM и таймеры

В проекте есть два FSM-сценария:

- `AcquaintanceState` — ожидание имени пользователя перед входом в меню.
- `SurveyState` — ожидание ответов анкеты.

Для timeout-логики используется `TimeoutManager` из `app/bot/cache/timeouts.py`. Он создаёт `asyncio.Task`, ждёт нужное количество секунд и вызывает callback, если таймер не отменили.

Важные правила при изменении сценариев:

- отменяйте старый таймер после корректного ответа пользователя;
- запускайте новый таймер после отправки следующего вопроса;
- очищайте FSM через `await state.clear()` при завершении или отмене сценария;
- для inline-вопросов анкеты задавайте `buttons` в `SurveyQuestion`, для текстовых — `min_length` и `max_length`.

---

## Анкета и AI-анализ

Вопросы анкеты описаны в `SURVEY_QUESTIONS` в `app/bot/services/survey.py`. Каждый вопрос содержит:

- `key` — ключ для сохранения ответа в FSM data;
- `title` и `text` — текст блока;
- `timeout_seconds` — время ожидания ответа;
- `min_length` / `max_length` — валидация текстовых ответов;
- `buttons` — inline-варианты, если вопрос не текстовый.

После последнего ответа `finish_survey()`:

1. Добавляет к данным сохранённое имя пользователя.
2. Отправляет пользователю сообщение об успешном заполнении.
3. Вызывает Groq-модель `openai/gpt-oss-20b` для структурирования анкеты.
4. При недоступности AI отправляет исходные ответы через fallback.
5. Сохраняет `raw_data` и `detailed_data` в таблицу `surveys`.
6. Отправляет анкету получателю из `SURVEY_RECEIVER_ID`.

---

## Работа с базой данных

Подключение собирается из переменных `POSTGRES_*` в `app/config.py` и используется в `app/db/session.py`.

Таблицы проекта:

| Модель | Таблица | Назначение |
| --- | --- | --- |
| `User` | `users` | Telegram ID, имя пользователя, флаги блокировки. |
| `Attachment` | `attachments` | Telegram `file_id` для локальных медиафайлов конкретного бота. |
| `SurveyData` | `surveys` | Сырые и структурированные ответы анкеты по `telegram_id`. |

`DbSessionMiddleware` автоматически добавляет `db_session` в аргументы хендлеров, делает `commit()` после успешной обработки и `rollback()` при ошибке.

Пример использования репозитория:

```python
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.repositories import users_repo

async def handler(db_session: AsyncSession, telegram_id: int) -> None:
    user = await users_repo.get_by_telegram_id(db_session, telegram_id=telegram_id)
```

После создания новой модели добавьте её импорт в `app/db/models/__init__.py`, чтобы Alembic видел таблицу при автогенерации.

---

## Миграции Alembic

Перед миграциями убедитесь, что PostgreSQL запущен, база создана, а `.env` заполнен.

```bash
# применить миграции
poetry run alembic upgrade head

# создать миграцию по моделям
poetry run alembic revision --autogenerate -m "migration name"

# создать пустую миграцию вручную
poetry run alembic revision -m "custom migration"

# посмотреть текущую ревизию БД
poetry run alembic current

# откатить последнюю миграцию
poetry run alembic downgrade -1
```

После автогенерации обязательно проверьте файл в `alembic/versions/` вручную.

---

## Полезные команды

```bash
# установить зависимости
poetry install

# запустить бота
poetry run python run.py

# применить миграции
poetry run alembic upgrade head

# проверить текущую ревизию БД
poetry run alembic current

# проверить синтаксис Python-файлов
poetry run python -m compileall app run.py
```

---

## Советы по разработке

- Один экран/раздел бота — один файл в `app/bot/handlers/` и отдельный `Router`.
- Callback data лучше делать предсказуемой: `section:action:id`, например `main_menu:results:1`.
- Не забывайте вызывать `await callback.answer()`, чтобы Telegram не показывал вечную загрузку на кнопке.
- Для длинных сценариев используйте FSM, а промежуточные данные храните в `FSMContext`.
- Любую работу с БД делайте через `db_session`, который приходит из middleware.
- Новые медиафайлы добавляйте не только в папку, но и в `ATTACHMENTS`.
- После изменения моделей всегда создавайте и проверяйте миграцию.
- Секреты не коммитьте: реальные значения должны быть только в локальном `.env`.
