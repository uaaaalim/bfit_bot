from aiogram.types import CallbackQuery

from core.implementations.button import BaseButton
from utils.menu_page import send_menu_page


class AboutMeButton(BaseButton):
    callback_data = "menu:about_me"

    async def execute(self, callback: CallbackQuery) -> None:
        if not callback.message:
            return

        await callback.message.delete()

        await send_menu_page(
            bot=self.client.bot,
            chat_id=callback.message.chat.id,
            text=(
                "👤 Обо мне\n\n"
                "Илья — персональный тренер\n"
                "Опыт в фитнесе: <b>более 15 лет</b>\n"
                "За это время через меня прошли сотни людей с разными целями и стартовыми условиями. "
                "Моя задача — не просто провести тренировку, <b>а довести до результата</b>.\n"
                "Работаю только с теми, кто готов вкладываться в процесс и брать ответственность за своё тело.\n\n"
                "💪 <b>Направления работы</b>:\n"
                "1. 🥊 Бокс\n"
                "2. 🤸‍♂️ Растяжка\n"
                "3. 🏃‍♂️‍➡️ Функциональный фитнес\n"
                "4. ⚖️ Похудение\n"
                "5. ⛹️ Коррекция осанки\n"
                "6. 💪 Набор мышечной массы\n\n"
                "⚖️ <b>Подход к работе</b>:\n"
                "— Без обещаний «быстрого результата»\n"
                "— Без лишних разговоров и давления\n"
                "— С уважением к твоему времени, здоровью и возможностям\n\n"
                "Каждая программа подстраивается под человека, а не наоборот.\n\n"
                "🎯 Результат: Сильное тело, выносливость, уверенность и понимание, "
                "как поддерживать форму без откатов назад.\n\n"
                "<b>Если ты готов работать — тогда заполняй анкету</b>. ✅"
            ),
            include_fill_form=True,
        )
