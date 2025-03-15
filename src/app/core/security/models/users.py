from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db.base.models import RecordModel


class User(RecordModel):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(100))
    surname: Mapped[str | None] = mapped_column(
        String(100), default=None, nullable=True
    )
    username: Mapped[str] = mapped_column(String(100), index=True, unique=True)
    hashed_password: Mapped[str]
    sessions: Mapped[List["UserSession"]] = relationship(back_populates="user")  # type: ignore # noqa
