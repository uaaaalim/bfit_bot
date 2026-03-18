from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from core.implementations.button import BaseButton


class DemoWaitButton(BaseButton):
    callback_data = "demo_wait_button"

    async def execute(self, callback: CallbackQuery) -> None:
        if not callback.message:
            await callback.answer("Нет исходного сообщения", show_alert=True)
            return

        await callback.answer()
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="Подтвердить", callback_data="confirm_action")]]
        )
        prompt = await callback.message.answer("Нажми 'Подтвердить' за 10 секунд", reply_markup=keyboard)

        async def on_timeout() -> None:
            await prompt.edit_text("⏰ Таймер истек. Кнопка не нажата")

        waited = await self.client.wait_for_button(
            chat_id=callback.message.chat.id,
            user_id=callback.from_user.id,
            timeout=10,
            on_timeout=on_timeout,
        )
        if waited and waited.data == "confirm_action":
            await waited.answer("Подтверждено")
            await prompt.edit_text("✅ Действие подтверждено")
