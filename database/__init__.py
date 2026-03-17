from sqlalchemy.ext.asyncio import AsyncSession

from database.repos.user_repo import UserRepository


class Repositories:
    def __init__(self, session: AsyncSession) -> None:
        self.users = UserRepository(session)
