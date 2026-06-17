import logging
from pathlib import Path

from aiogram import Bot
from aiogram.types import FSInputFile

from app.bot.cache.attachments import AttachmentsMemoryCache
from app.config import get_settings
from app.db import get_session
from app.db.models import FileType
from app.db.repositories import media_cache_repo

PHOTOS = {
    "main_menu": Path("app/attachments/images/main_menu.jpg")
}

settings = get_settings()
logger = logging.getLogger(__name__)


async def check_attachments(bot: Bot, memory_cache: AttachmentsMemoryCache) -> None:
    async with get_session() as session:
        for photo_path in PHOTOS.values():
            normalized_path = photo_path.as_posix()

            cached_media = await media_cache_repo.get_by_path(
                session=session,
                path=normalized_path,
            )

            if cached_media is not None:
                logger.info(
                    "Photo already cached: path=%s",
                    normalized_path,
                )
                continue

            if not photo_path.exists():
                raise FileNotFoundError(
                    f"Attachment not found: {normalized_path}"
                )

            logger.info(
                "Uploading photo to chat: path=%s",
                normalized_path,
            )

            sent_message = await bot.send_photo(
                chat_id=settings.media_check_victim_id,
                photo=FSInputFile(photo_path),
                caption=f"Cached new photo: {normalized_path}",
            )

            if not sent_message.photo:
                raise RuntimeError(
                    f"Telegram did not return photo data: {normalized_path}"
                )

            file_id = sent_message.photo[-1].file_id

            await media_cache_repo.create(
                session=session,
                bot_id=bot.id,
                path=normalized_path,
                type_=FileType.IMAGE,
                file_id=file_id,
            )

            logger.info(
                "Photo cached: path=%s",
                normalized_path,
            )

        media_items = await media_cache_repo.get_all(session)

        memory_cache.load_many(
            {
                media.path: media.media_id
                for media in media_items
            }
        )

        logger.info("Loaded %s media items from database into memory cache", len(media_items))
