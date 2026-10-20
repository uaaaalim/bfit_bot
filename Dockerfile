FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Poetry устанавливается отдельно от зависимостей бота.
RUN pip install --no-cache-dir poetry==2.3.2

# Этот слой пересобирается только при изменении зависимостей.
COPY pyproject.toml poetry.lock ./
RUN poetry install --only main --no-root --no-ansi

COPY app ./app
COPY alembic ./alembic
COPY alembic.ini run.py ./

# Запускаем бота от обычного пользователя.
RUN useradd --create-home --uid 10001 bfit \
    && mkdir -p /app/logs \
    && chown bfit:bfit /app/logs

USER bfit

CMD ["python", "run.py"]