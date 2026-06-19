from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

status_router = Router(name="status")

@status_router.message(Command("status"))
async def status(message: Message, db_session: AsyncSession) -> None:
    pass
