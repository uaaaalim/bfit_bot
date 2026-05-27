from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import Settings


def create_bot(settings: Settings) -> Bot:
    return Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
        ),
    )


def create_dispatcher() -> Dispatcher:
    dp = Dispatcher()

    # Позже сюда добавим:
    # - storage для FSM
    # - middlewares
    # - routers

    return dp