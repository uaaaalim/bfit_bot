from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from core.database.base import BaseEntity


class User(BaseEntity):
    __tablename__ = "users"

    tg_id: Mapped[int] = mapped_column(unique=True, index=True)
    username: Mapped[str | None] = mapped_column(String(255), nullable=True)
