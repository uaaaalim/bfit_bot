# bfit_bot

Базовый и читаемый шаблон Telegram-бота на:
- Python 3.13.7
- aiogram 3
- SQLAlchemy (async)
- Alembic
- PostgreSQL

## Что важно в этой версии
- `commands`, `buttons`, `messages`, `schedules` загружаются **автоматически через чтение директорий**.
- `client` передается в каждый handler-класс (`BaseCommand`, `BaseButton`, `BaseMessage`, `BaseSchedule`).
- Проверка `from_user` вынесена в Base-классы (`handle`), поэтому в командах не нужно писать `if not message.from_user: return`.
- Временное ожидание (message/button) поддерживает timeout и изменение текста сообщения при истечении таймера.
- Лог-формат: `2026-03-17 11:30:00 [INFO  ] message`.

## Установка
```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Миграции
```bash
alembic upgrade head
```

## Запуск
```bash
python run.py
```

## Автозагрузка из директорий
Загрузка идет через `core/loader.py` + `Path("commands").glob("*.py")` и т.д.

## Пример ожидания сообщения
Команда `/wait_message` (`commands/wait_message.py`):
```python
prompt = await message.answer("Отправь любое сообщение в течение 10 секунд")

async def on_timeout() -> None:
    await prompt.edit_text("⏰ Таймер истек. Сообщение не получено")

waited = await self.client.wait_for_message(...)
if waited:
    await prompt.edit_text("✅ Сообщение получено вовремя")
```

## Пример ожидания кнопки
Кнопка `demo_wait_button` (`buttons/demo_wait_button.py`):
```python
prompt = await callback.message.answer("Нажми 'Подтвердить' за 10 секунд", reply_markup=keyboard)

async def on_timeout() -> None:
    await prompt.edit_text("⏰ Таймер истек. Кнопка не нажата")

waited = await self.client.wait_for_button(...)
if waited and waited.data == "confirm_action":
    await prompt.edit_text("✅ Действие подтверждено")
```

## Пример БД: создание entity и запрос
Команда `/db_demo` (`commands/db_demo.py`):
```python
async with self.client.db.session() as session:
    repos = Repositories(session)
    user = await repos.users.get_where(User.tg_id == message.from_user.id)
    if not user:
        user = await repos.users.create(User(...))
```

## Логи при старте
`run.py` выводит:
- имя модуля
- версию проекта
- git short hash
- версии Python / aiogram / sqlalchemy / alembic
- ивенты загрузки handlers/schedules и запуск polling
