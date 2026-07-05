from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base

class SurveyData(Base):
    __tablename__ = 'surveys'

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        unique=True,
        nullable=False
    )

    telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        unique=True
    )

    raw_data: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    detailed_data: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
