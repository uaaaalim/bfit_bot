from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from core.implementations.button import BaseButton
from utils.main_menu import send_main_menu


class FillFormButton(BaseButton):
    callback_data = "menu:fill_form"

    _direction_options = {
        "survey_direction_gym": "🏋️Фитнес-качалка",
        "survey_direction_functional": "🔥Функциональные тренировки",
        "survey_direction_boxing": "🥊 Бокс",
        "survey_direction_stretch": "🤸Растяжка-гибкость",
    }

    async def execute(self, callback: CallbackQuery) -> None:
        if not callback.message:
            await callback.answer("Не удалось открыть анкету", show_alert=True)
            return

        await callback.answer()

        chat_id = callback.message.chat.id
        await callback.message.delete()
        user_id = callback.from_user.id

        intro = (
            "📋 Подберём тебе идеальный формат тренировок 💪\n"
            "Перед началом тренировок хочу немного узнать тебя, "
            "чтобы сделать максимально эффективную и безопасную программу 🧠\n\n"
            "➡️ Ответь, пожалуйста, на несколько простых вопросов:"
        )
        await callback.message.answer(intro)

        name = await self._ask_name(chat_id=chat_id, user_id=user_id)
        if name is None:
            await send_main_menu(self.client.bot, chat_id)
            return

        purpose = await self._ask_purpose(chat_id=chat_id, user_id=user_id)
        if purpose is None:
            await send_main_menu(self.client.bot, chat_id)
            return

        direction = await self._ask_direction(chat_id=chat_id, user_id=user_id)
        if direction is None:
            await send_main_menu(self.client.bot, chat_id)
            return

        restrictions = await self._ask_restrictions(chat_id=chat_id, user_id=user_id)
        if restrictions is None:
            await send_main_menu(self.client.bot, chat_id)
            return

        summary = (
            "✅ Анкета заполнена!\n\n"
            f"1. Имя: {name}\n"
            f"2. Цель: {purpose}\n"
            f"3. Направление: {direction}\n"
            f"4. Травмы/ограничения: {restrictions}\n\n"
            "❗ Ожидай обязательно ответа, мы свяжемся."
        )
        await callback.message.answer(summary)

        if self.client.config.author_id:
            if not callback.from_user.username:
                link = f'<a href="tg://user?id={callback.from_user.id}">{callback.from_user.full_name}</a>'
            else:
                link = f'@{callback.from_user.username} ({callback.from_user.full_name})'

            await callback.bot.send_message(
                self.client.config.author_id,
                f"🆕 <b>НОВАЯ АНКЕТА</b> от {link}\n\n"
                f"Данные анкеты:\n"
                f"1. Имя: {name}\n"
                f"2. Цель: {purpose}\n"
                f"3. Направление: {direction}\n"
                f"4. Травмы или ограничения: {restrictions}",
                parse_mode="HTML"
            )

        await send_main_menu(self.client.bot, chat_id)

    async def _ask_name(self, chat_id: int, user_id: int) -> str | None:
        while True:
            _msg = await self.client.bot.send_message(chat_id, "➡️ Как тебя зовут? 🙂")
            message = await self._wait_message(chat_id=chat_id, user_id=user_id)
            if message is None:
                return None

            if not self._is_text_message(message):
                await self.client.bot.send_message(
                    chat_id,
                    "Ответ должен быть текстом. Введи имя от 2 до 15 символов.",
                )
                continue

            name = message.text.strip()
            if len(name) < 2 or len(name) > 15:
                await self.client.bot.send_message(
                    chat_id,
                    "Некорректное имя: нужно от 2 до 15 символов. Попробуй ещё раз.",
                )
                continue

            await _msg.delete()
            return name

    async def _ask_purpose(self, chat_id: int, user_id: int) -> str | None:
        while True:
            _msg = await self.client.bot.send_message(chat_id, "➡️ Какая у тебя цель?")
            message = await self._wait_message(chat_id=chat_id, user_id=user_id)
            if message is None:
                return None

            if not self._is_text_message(message):
                await self.client.bot.send_message(chat_id, "Ответ должен быть текстом. Попробуй снова.")
                continue

            purpose = message.text.strip()
            if len(purpose) > 100:
                await self.client.bot.send_message(
                    chat_id,
                    "Слишком длинный ответ: цель должна быть не более 100 символов. Попробуй ещё раз.",
                )
                continue
            if not purpose:
                await self.client.bot.send_message(chat_id, "Пустой ответ не подходит. Напиши свою цель.")
                continue

            await _msg.delete()
            return purpose

    async def _ask_direction(self, chat_id: int, user_id: int) -> str | None:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="🏋️ Фитнес-качалка", callback_data="survey_direction_gym"),
                    InlineKeyboardButton(text="🔥 Функциональные тренировки", callback_data="survey_direction_functional"),
                ],
                [
                    InlineKeyboardButton(text="🥊 Бокс", callback_data="survey_direction_boxing"),
                    InlineKeyboardButton(text="🤸 Растяжка-гибкость", callback_data="survey_direction_stretch"),
                ],
            ]
        )

        prompt = await self.client.bot.send_message(
            chat_id,
            "➡️ Какое направление тебе ближе?",
            reply_markup=keyboard,
        )

        async def on_timeout() -> None:
            await prompt.edit_text("⏰ Время вышло. Запусти анкету заново.")

        while True:
            pressed = await self.client.wait_for_button(
                chat_id=chat_id,
                user_id=user_id,
                timeout=30,
                on_timeout=on_timeout,
            )
            if pressed is None:
                return None

            if pressed.data not in self._direction_options:
                await pressed.answer("Выбери вариант только из анкеты", show_alert=True)
                continue

            await pressed.answer()
            await prompt.delete()
            return self._direction_options[pressed.data]

    async def _ask_restrictions(self, chat_id: int, user_id: int) -> str | None:
        while True:
            _msg = await self.client.bot.send_message(chat_id, "➡️ Есть ли травмы или ограничения по здоровью?")
            message = await self._wait_message(chat_id=chat_id, user_id=user_id)
            if message is None:
                return None

            if not self._is_text_message(message):
                await self.client.bot.send_message(chat_id, "Ответ должен быть текстом. Попробуй снова.")
                continue

            restrictions = message.text.strip()
            if len(restrictions) > 100:
                await self.client.bot.send_message(
                    chat_id,
                    "Слишком длинный ответ: ограничения по здоровью должны быть до 100 символов.",
                )
                continue
            if not restrictions:
                await self.client.bot.send_message(
                    chat_id,
                    "Пустой ответ не подходит. Если ограничений нет, напиши 'Нет'.",
                )
                continue

            await _msg.delete()
            return restrictions

    async def _wait_message(self, chat_id: int, user_id: int) -> Message | None:
        async def on_timeout() -> None:
            await self.client.bot.send_message(chat_id, "⏰ Время ожидания вышло. Запусти анкету заново.")

        return await self.client.wait_for_message(
            chat_id=chat_id,
            user_id=user_id,
            timeout=30,
            on_timeout=on_timeout,
        )

    @staticmethod
    def _is_text_message(message: Message) -> bool:
        return bool(message.text and message.text.strip())
