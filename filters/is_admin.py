import logging

from aiogram.filters import BaseFilter
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession

from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class IsAdminFilter(BaseFilter):
    def __init__(self) -> None:
        self.admin_ids = settings.admins

    async def __call__(
            self, event: TelegramObject, db_session: AsyncSession
    ):
        if not hasattr(event, 'from_user'):
            return False

        user_id = event.from_user.id

        if user_id in self.admin_ids:
            logger.info(f'User id={user_id} granted admin access via config')
            return True

        logger.warning(f'User id={user_id} attempted admin access without permission')
        return False