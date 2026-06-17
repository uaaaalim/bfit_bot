from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.media_cache import MediaCache, FileType


async def get_all(session: AsyncSession) -> list[MediaCache]:
    stmt = select(MediaCache).order_by(MediaCache.id)

    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_by_path(session: AsyncSession, path: str) -> MediaCache | None:
    stmt = select(MediaCache).where(MediaCache.path == path)

    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def create(
    session: AsyncSession,
    *,
    bot_id: int,
    path: str,
    type_: FileType,
    file_id: str,
) -> MediaCache:
    media = MediaCache(
        bot_id=bot_id,
        path=path,
        file_type=type_,
        media_id=file_id,
    )

    session.add(media)
    await session.flush()

    return media


async def update(
    session: AsyncSession,
    media: MediaCache,
    *,
    path: str | None = None,
    type_: str | None = None,
    file_id: str | None = None,
) -> MediaCache:
    if path is not None:
        media.path = path

    if type_ is not None:
        media.type = type_

    if file_id is not None:
        media.file_id = file_id

    await session.flush()

    return media
