from uuid import uuid4, UUID
from datetime import datetime
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import TIMESTAMP
from app.core.timezone import utc_now


class IntegerPrimaryKeyMixin:
    id: Mapped[int] = mapped_column(default=None, primary_key=True)


class UUIDPrimaryKeyMixin:
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)


class CreatedAtMixin:
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, default=utc_now, index=True
    )


class UpdatedAtMixin:
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )


class TimestampMixin(CreatedAtMixin, UpdatedAtMixin): ...


class SoftDeleteMixin:
    deleted_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=None, nullable=True
    )

    def delete(self) -> None:
        self.deleted_at = utc_now()

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None
