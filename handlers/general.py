from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from filters.is_admin import IsAdminFilter

general_router = Router(name='general_router')

@general_router.message(CommandStart(), IsAdminFilter())
async def command_start(message: Message):
    await message.reply("Hello, World!")