import logging
from dataclasses import dataclass
from pathlib import Path

from aiogram import Bot
from aiogram.types import FSInputFile

from app.bot.cache import attachments_cache
from app.config import get_settings
from app.db import get_session
from app.db.models import FileType
from app.db.repositories import attachments_repo


logger = logging.getLogger(__name__)
settings = get_settings()


@dataclass(frozen=True)
class AttachmentFile:
    path: Path
    type: FileType


ATTACHMENTS: list[AttachmentFile] = [
    AttachmentFile(
        path=Path("app/attachments/images/main_menu.jpg"),
        type=FileType.IMAGE,
    ),
    AttachmentFile(
        path=Path("app/attachments/images/about.jpg"),
        type=FileType.IMAGE,
    ),
    AttachmentFile(
        path=Path("app/attachments/images/qualification.jpg"),
        type=FileType.IMAGE,
    ),
    AttachmentFile(
        path=Path("app/attachments/images/documents/banzai_fitness_seminar.png"),
        type=FileType.IMAGE,
    ),
    AttachmentFile(
        path=Path("app/attachments/images/documents/invictus_academy_certificate.png"),
        type=FileType.IMAGE,
    ),
    AttachmentFile(
        path=Path("app/attachments/images/documents/qualification_school.jpg"),
        type=FileType.IMAGE,
    ),
    AttachmentFile(
        path=Path("app/attachments/images/documents/sport_forum_diploma.jpg"),
        type=FileType.IMAGE,
    ),

    # пример видео
    # Attachment(
    #     path=Path("app/attachments/videos/intro.mp4"),
    #     type=FileType.VIDEO,
    # ),
]


async def upload_attachment(
    bot: Bot,
    attachment: AttachmentFile,
) -> str:
    normalized_path = attachment.path.as_posix()

    if not attachment.path.exists():
        raise FileNotFoundError(f"Attachment not found: {normalized_path}")

    file = FSInputFile(attachment.path)

    if attachment.type == FileType.IMAGE:
        sent_message = await bot.send_photo(
            chat_id=settings.media_check_victim_id,
            photo=file,
            caption=f"Cached new photo: {normalized_path}",
        )

        if not sent_message.photo:
            raise RuntimeError(f"Telegram did not return photo data: {normalized_path}")

        return sent_message.photo[-1].file_id

    if attachment.type == FileType.VIDEO:
        sent_message = await bot.send_video(
            chat_id=settings.media_check_victim_id,
            video=file,
            caption=f"Cached new video: {normalized_path}",
        )

        if sent_message.video is None:
            raise RuntimeError(f"Telegram did not return video data: {normalized_path}")

        return sent_message.video.file_id

    raise ValueError(f"Unsupported attachment type: {attachment.type}")


async def check_attachments(bot: Bot) -> None:
    async with get_session() as session:
        bot_info = await bot.get_me()
        bot_id = bot_info.id

        media_items = await attachments_repo.get_all_by_bot_id(
            session=session,
            bot_id=bot_id,
        )

        attachments_cache.load_many(
            {
                item.path: item.file_id
                for item in media_items
            }
        )

        existing_paths = {
            item.path
            for item in media_items
        }

        logger.info(
            "Loaded %s media items from database into memory cache",
            len(media_items),
        )

        for attachment in ATTACHMENTS:
            normalized_path = attachment.path.as_posix()

            if normalized_path in existing_paths:
                logger.info("Attachment already cached: path=%s", normalized_path)
                continue

            logger.info("Uploading attachment: path=%s", normalized_path)

            file_id = await upload_attachment(
                bot=bot,
                attachment=attachment,
            )

            await attachments_repo.create(
                session=session,
                bot_id=bot_id,
                path=normalized_path,
                type_=attachment.type,
                file_id=file_id,
            )

            attachments_cache.set(normalized_path, file_id)
            existing_paths.add(normalized_path)

            logger.info("Attachment cached: path=%s", normalized_path)
