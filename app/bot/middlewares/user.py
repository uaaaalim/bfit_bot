import logging
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User as TelegramUser
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories import users_repo


logger = logging.getLogger(__name__)


class UserCheckMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        logger.info("Middleware loaded")

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        db_session: AsyncSession | None = data.get("db_session")
        event_from_user: TelegramUser | None = data.get("event_from_user")

        if db_session is None:
            logger.warning("Check is skipped: db_session not found")
            return await handler(event, data)

        if event_from_user is None:
            return await handler(event, data)

        await users_repo.get_or_create(
            session=db_session,
            telegram_id=event_from_user.id
        )
        return await handler(event, data)