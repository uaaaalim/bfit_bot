from sqlalchemy import Sequence, BigInteger, Boolean, String
from sqlalchemy.orm import mapped_column, Mapped

from app.db import TimestampMixin, Base

user_id_sequence = Sequence('user_id_sequence', start=1000, increment=1)


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        BigInteger,
        user_id_sequence,
        server_default=user_id_sequence.next_value(),
        primary_key=True,
        unique=True,
        nullable=False
    )

    telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    is_blocked: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    block_reason: Mapped[str] = mapped_column(
        String, nullable=True
    )
