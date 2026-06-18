from enum import StrEnum

from sqlalchemy import Enum, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class FileType(StrEnum):
    IMAGE = "image"
    VIDEO = "video"


class Attachment(Base, TimestampMixin):
    __tablename__ = "attachments"

    id: Mapped[int] = mapped_column(primary_key=True)

    bot_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    path: Mapped[str] = mapped_column(
        String(500),
        unique=True,
        nullable=False,
    )

    file_type: Mapped[FileType] = mapped_column(
        Enum(
            FileType,
            name="file_type_enum",
        ),
        nullable=False,
    )

    file_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
