from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User


async def get_by_telegram_id(
    session: AsyncSession,
    telegram_id: int,
) -> User | None:
    stmt = select(User).where(User.telegram_id == telegram_id)

    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def create(
    session: AsyncSession,
    *,
    telegram_id: int
) -> User:
    user = User(
        telegram_id=telegram_id,
        is_blocked=False,
    )

    session.add(user)
    await session.flush()

    return user


async def get_or_create(
    session: AsyncSession,
    *,
    telegram_id: int
) -> User:
    user = await get_by_telegram_id(
        session=session,
        telegram_id=telegram_id,
    )

    if user is not None:
        return user

    return await create(
        session=session,
        telegram_id=telegram_id,
    )


async def set_passed_survey(
        session: AsyncSession,
        *,
        telegram_id: int,
        value: bool = True
) -> None:
    stmt = (
        update(User)
        .where(User.telegram_id == telegram_id)
        .values(passed_survey=value)
    )

    await session.execute(stmt)
