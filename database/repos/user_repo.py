from sqlalchemy.ext.asyncio import AsyncSession

from core.database.crud import CRUDRepository
from database.entities.user import User


class UserRepository(CRUDRepository[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(User, session)
