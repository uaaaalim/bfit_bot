from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

from bot.core.active_action import get_active_action

ACTIVE_ACTION_TEXT = "У вас уже есть активное действие. Завершите его или дождитесь таймаута."


class ActiveActionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        if isinstance(event, CallbackQuery):
            user_id = event.from_user.id
            action = get_active_action(user_id)
            if action is None:
                return await handler(event, data)

            if action.kind == "button" and event.data == action.callback_data:
                return await handler(event, data)

            await event.answer(ACTIVE_ACTION_TEXT, show_alert=True)
            return None

        if isinstance(event, Message):
            user = event.from_user
            if user is None:
                return await handler(event, data)

            action = get_active_action(user.id)
            if action is None:
                return await handler(event, data)

            if action.kind == "message" and not (event.text or "").startswith("/"):
                return await handler(event, data)

            await event.answer(ACTIVE_ACTION_TEXT)
            return None

        return await handler(event, data)
