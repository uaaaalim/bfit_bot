from aiogram.types import Message

from core.implementations.message import BaseMessage


class EchoMessage(BaseMessage):
    trigger = "*"

    async def execute(self, message: Message) -> None:
        if message.text and not message.text.startswith("/"):
            await message.answer(f"Эхо: {message.text}")
