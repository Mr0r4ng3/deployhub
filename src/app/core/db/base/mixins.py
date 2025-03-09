from uuid import uuid4, UUID
from datetime import datetime
from sqlmodel import Column, Field, DateTime
from app.core.timezone import utc_now


class IntegerPrimaryKeyMixin:
    id: int | None = Field(default=None, primary_key=True)


class UUIDPrimaryKeyMixin:
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)


class CreatedAtMixin:
    created_at: datetime | None = Field(
        nullable=False,
        default_factory=utc_now,
        sa_type=DateTime(timezone=True),
    )


class UpdatedAtMixin:
    updated_at: datetime | None = Field(
        nullable=False,
        default_factory=utc_now,
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={"onupdate": utc_now},
    )


class TimestampMixin(CreatedAtMixin, UpdatedAtMixin): ...


class SoftDeleteMixin:
    deleted_at: datetime | None = Field(
        default=None, nullable=True, sa_type=DateTime(timezone=True)
    )

    def delete(self) -> None:
        self.deleted_at = utc_now()

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None
