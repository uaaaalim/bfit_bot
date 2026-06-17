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
    width: int | None = None
    height: int | None = None

    @property
    def normalized_path(self) -> str:
        return self.path.as_posix()


ATTACHMENTS: list[AttachmentFile] = [
    # MENU
    AttachmentFile(Path("app/attachments/main_menu.jpg"), FileType.IMAGE),
    AttachmentFile(Path("app/attachments/about.jpg"), FileType.IMAGE),
    AttachmentFile(Path("app/attachments/qualification.jpg"), FileType.IMAGE),
    AttachmentFile(Path("app/attachments/documents/banzai_fitness_seminar.png"), FileType.IMAGE),
    AttachmentFile(Path("app/attachments/documents/invictus_academy_certificate.png"), FileType.IMAGE),
    AttachmentFile(Path("app/attachments/documents/qualification_school.jpg"), FileType.IMAGE),
    AttachmentFile(Path("app/attachments/documents/sport_forum_diploma.jpg"), FileType.IMAGE),

    # RESULTS
    AttachmentFile(Path("app/attachments/results/photo_2026-06-17_23-14-47.jpg"), FileType.IMAGE),
    AttachmentFile(Path("app/attachments/results/photo_2026-06-17_23-16-33.jpg"), FileType.IMAGE),
    AttachmentFile(Path("app/attachments/results/video1.mp4"), FileType.VIDEO, width=720, height=1280),
    AttachmentFile(Path("app/attachments/results/video2.mp4"), FileType.VIDEO),
]


async def upload_attachment(
    bot: Bot,
    attachment: AttachmentFile,
) -> str:
    normalized_path = attachment.normalized_path

    if not attachment.path.exists():
        raise FileNotFoundError(f"Attachment not found: {normalized_path}")

    file = FSInputFile(attachment.path)

    if attachment.type == FileType.IMAGE:
        sent_message = await bot.send_photo(
            chat_id=settings.media_check_victim_id,
            photo=file,
            caption=f"Cached new image: {normalized_path}",
        )

        if not sent_message.photo:
            raise RuntimeError(f"Telegram did not return photo data: {normalized_path}")

        return sent_message.photo[-1].file_id

    if attachment.type == FileType.VIDEO:
        sent_message = await bot.send_video(
            chat_id=settings.media_check_victim_id,
            video=file,
            caption=f"Cached new video: {normalized_path}",
            width=attachment.width,
            height=attachment.height,
        )

        if sent_message.video is None:
            raise RuntimeError(f"Telegram did not return video data: {normalized_path}")

        return sent_message.video.file_id

    raise ValueError(f"Unsupported attachment type: {attachment.type}")


async def check_attachments(bot: Bot) -> None:
    logger.info("Starting attachments check...")

    async with get_session() as session:
        bot_info = await bot.get_me()
        bot_id = bot_info.id

        declared_attachments = {
            attachment.normalized_path: attachment
            for attachment in ATTACHMENTS
        }

        declared_paths = set(declared_attachments.keys())

        media_items = await attachments_repo.get_all_by_bot_id(
            session=session,
            bot_id=bot_id,
        )

        db_paths = {
            item.path
            for item in media_items
        }

        attachments_cache.clear()

        attachments_cache.load_many(
            {
                item.path: item.file_id
                for item in media_items
                if item.path in declared_paths
            }
        )

        logger.info(
            "Loaded attachments from database: total=%s, valid=%s",
            len(media_items),
            len(db_paths & declared_paths),
        )

        stale_paths = db_paths - declared_paths

        if stale_paths:
            deleted_count = await attachments_repo.delete_by_paths(
                session=session,
                bot_id=bot_id,
                paths=stale_paths,
            )

            for stale_path in stale_paths:
                attachments_cache.delete(stale_path)

            logger.warning(
                "Deleted stale attachments from database: count=%s paths=%s",
                deleted_count,
                sorted(stale_paths),
            )
        else:
            logger.info("No stale attachments found")

        cached_new = 0
        skipped_existing = 0
        missing_files = 0

        for attachment in ATTACHMENTS:
            normalized_path = attachment.normalized_path

            if normalized_path in db_paths:
                logger.debug("Attachment already cached: path=%s", normalized_path)
                skipped_existing += 1
                continue

            if not attachment.path.exists():
                logger.error("Attachment file does not exist: path=%s", normalized_path)
                missing_files += 1
                raise FileNotFoundError(f"Attachment not found: {normalized_path}")

            logger.info(
                "Uploading new attachment: type=%s path=%s",
                attachment.type.value,
                normalized_path,
            )

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
            db_paths.add(normalized_path)

            cached_new += 1

            logger.info(
                "Attachment cached: type=%s path=%s",
                attachment.type.value,
                normalized_path,
            )

        logger.info(
            "Attachments check finished: declared=%s, skipped=%s, uploaded=%s, deleted_stale=%s, missing=%s",
            len(ATTACHMENTS),
            skipped_existing,
            cached_new,
            len(stale_paths),
            missing_files,
        )