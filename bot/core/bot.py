import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.core import configuration
from bot.handlers import ROUTERS

logger = logging.getLogger(__name__)


class Client:
    bot: Bot = Bot(
        token=configuration.telegram_token.get_secret_value(),
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
            link_preview_is_disabled=True,
        )
    )
    dp: Dispatcher = Dispatcher()

    def load_routes(self) -> None:
        for router in ROUTERS:
            self.dp.include_router(router)
        logger.info("{} routers are loaded".format(len(ROUTERS)))

    async def run(self) -> None:
        logger.info("Starting polling...")
        await self.bot.delete_webhook(drop_pending_updates=True)
        await self.dp.start_polling(self.bot)

    async def shutdown(self) -> None:
        await self.bot.session.close()
