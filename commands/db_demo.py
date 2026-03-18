from aiogram.types import Message

from core.implementations.command import BaseCommand
from database import Repositories
from database.entities.user import User


class DbDemoCommand(BaseCommand):
    name = "db_demo"
    description = "Пример работы с БД"

    async def execute(self, message: Message) -> None:
        async with self.client.db.session() as session:
            repos = Repositories(session)
            user = await repos.users.get_where(User.tg_id == message.from_user.id)
            if not user:
                user = User(tg_id=message.from_user.id, username=message.from_user.username)
                user = await repos.users.create(user)
                await message.answer(f"Создан пользователь с id={user.id}")
                return

            await message.answer(f"Пользователь найден: id={user.id}, username={user.username}")
