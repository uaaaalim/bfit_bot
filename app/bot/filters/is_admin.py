from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery


class AdminFilter(BaseFilter):
    def __init__(self, admin_ids: list[int]) -> None:
        self.admin_ids = admin_ids

    async def __call__(self, event: Message | CallbackQuery) -> bool:
        user = event.from_user

        if user is None:
            return False

        return user.id in self.admin_ids
