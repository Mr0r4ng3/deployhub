from datetime import datetime
from sqlmodel import Field, DateTime
from app.core.timezone import utc_now


class IntegerPrimaryKeyMixin:
    id: int | None = Field(default=None, primary_key=True)


class CreatedAtMixin:
    created_at: datetime | None = Field(default_factory=utc_now)


class UpdatedAtMixin:
    updated_at: datetime | None = Field(
        default_factory=utc_now, sa_column_kwargs={"onupdate": utc_now}, nullable=False
    )


class TimestampMixin(CreatedAtMixin, UpdatedAtMixin): ...


class SoftDeleteMixin:
    deleted_at: datetime | None = Field(default=None, sa_type=DateTime())

    def delete(self) -> None:
        self.deleted_at = utc_now()
