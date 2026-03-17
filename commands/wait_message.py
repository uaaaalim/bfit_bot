from aiogram.types import Message

from core.implementations.command import BaseCommand


class WaitMessageCommand(BaseCommand):
    name = "wait_message"
    description = "Ожидание сообщения 10 секунд"

    async def execute(self, message: Message) -> None:
        prompt = await message.answer("Отправь любое сообщение в течение 10 секунд")

        async def on_timeout() -> None:
            await prompt.edit_text("⏰ Таймер истек. Сообщение не получено")
            await message.answer("Можно запустить /wait_message еще раз")

        waited = await self.client.wait_for_message(
            chat_id=message.chat.id,
            user_id=message.from_user.id,
            timeout=10,
            on_timeout=on_timeout,
        )
        if waited:
            await prompt.edit_text("✅ Сообщение получено вовремя")
            await message.answer(f"Получено: {waited.text}")
