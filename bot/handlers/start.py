from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

start_router = Router(name="start")

@start_router.message(CommandStart())
async def start(message: Message):
    await message.answer("HI!")