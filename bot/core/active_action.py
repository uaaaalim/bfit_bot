import asyncio
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any, Literal

from aiogram import Bot

ActionKind = Literal["button", "message"]
TimeoutHandler = Callable[[Bot, int], Awaitable[None]]


@dataclass
class ActiveAction:
    kind: ActionKind
    task: asyncio.Task[None]
    callback_data: str | None = None


_ACTIVE_ACTIONS: dict[int, ActiveAction] = {}


def get_active_action(user_id: int) -> ActiveAction | None:
    return _ACTIVE_ACTIONS.get(user_id)


def has_active_action(user_id: int) -> bool:
    return user_id in _ACTIVE_ACTIONS


def finish_action(user_id: int) -> None:
    action = _ACTIVE_ACTIONS.pop(user_id, None)
    if action and not action.task.done():
        action.task.cancel()


def start_action(
    *,
    bot: Bot,
    user_id: int,
    kind: ActionKind,
    timeout: int,
    on_timeout: TimeoutHandler,
    callback_data: str | None = None,
) -> None:
    finish_action(user_id)

    async def wait_timeout() -> None:
        try:
            await asyncio.sleep(timeout)
        except asyncio.CancelledError:
            return

        if _ACTIVE_ACTIONS.pop(user_id, None) is not None:
            await on_timeout(bot, user_id)

    _ACTIVE_ACTIONS[user_id] = ActiveAction(
        kind=kind,
        task=asyncio.create_task(wait_timeout()),
        callback_data=callback_data,
    )
