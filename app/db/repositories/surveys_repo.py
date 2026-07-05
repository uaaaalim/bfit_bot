from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import SurveyData


async def get_by_telegram_id(
    session: AsyncSession,
    telegram_id: int,
) -> SurveyData | None:
    stmt = select(SurveyData).where(SurveyData.telegram_id == telegram_id)

    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def set_data(
    session: AsyncSession,
    *,
    telegram_id: int,
    raw_data: str,
    detailed_data: str,
) -> SurveyData:
    survey_data = await get_by_telegram_id(
        session=session,
        telegram_id=telegram_id,
    )

    if survey_data is None:
        survey_data = SurveyData(
            telegram_id=telegram_id,
            raw_data=raw_data,
            detailed_data=detailed_data,
        )
        session.add(survey_data)
    else:
        survey_data.raw_data = raw_data
        survey_data.detailed_data = detailed_data

    await session.flush()
    return survey_data
