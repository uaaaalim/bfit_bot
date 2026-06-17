from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Attachments, FileType


async def get_all_by_bot_id(
    session: AsyncSession,
    bot_id: int,
) -> list[Attachments]:
    stmt = (
        select(Attachments)
        .where(Attachments.bot_id == bot_id)
        .order_by(Attachments.id)
    )

    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_by_path(
    session: AsyncSession,
    *,
    bot_id: int,
    path: str,
) -> Attachments | None:
    stmt = select(Attachments).where(
        Attachments.bot_id == bot_id,
        Attachments.path == path,
    )

    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def create(
    session: AsyncSession,
    *,
    bot_id: int,
    path: str,
    type_: FileType,
    file_id: str,
) -> Attachments:
    item = Attachments(
        bot_id=bot_id,
        path=path,
        file_type=type_,
        file_id=file_id,
    )

    session.add(item)
    await session.flush()

    return item


async def create_or_update(
    session: AsyncSession,
    *,
    bot_id: int,
    path: str,
    type_: FileType,
    file_id: str,
) -> Attachments:
    item = await get_by_path(
        session=session,
        bot_id=bot_id,
        path=path,
    )

    if item is None:
        return await create(
            session=session,
            bot_id=bot_id,
            path=path,
            type_=type_,
            file_id=file_id,
        )

    item.type = type_.value
    item.file_id = file_id

    await session.flush()

    return item


async def delete_by_paths(
    session: AsyncSession,
    *,
    bot_id: int,
    paths: set[str],
) -> int:
    if not paths:
        return 0

    stmt = delete(Attachments).where(
        Attachments.bot_id == bot_id,
        Attachments.path.in_(paths),
    )

    result = await session.execute(stmt)

    return result.rowcount or 0