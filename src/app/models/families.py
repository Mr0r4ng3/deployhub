from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db.base.models import RecordModel


class Family(RecordModel):
    __tablename__ = "families"

    name: Mapped[str] = mapped_column(String(100), index=True, unique=True)
