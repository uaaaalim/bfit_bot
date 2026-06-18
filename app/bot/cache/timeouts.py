import asyncio
from collections.abc import Awaitable, Callable


class TimeoutManager:
    def __init__(self) -> None:
        self._tasks: dict[int, asyncio.Task] = {}

    def cancel(self, user_id: int) -> None:
        task = self._tasks.pop(user_id, None)

        if task and not task.done():
            task.cancel()

    def start(
        self,
        user_id: int,
        timeout_seconds: int,
        callback: Callable[[], Awaitable[None]],
    ) -> None:
        self.cancel(user_id)

        async def waiter() -> None:
            try:
                await asyncio.sleep(timeout_seconds)
                await callback()
            except asyncio.CancelledError:
                return

        self._tasks[user_id] = asyncio.create_task(waiter())
