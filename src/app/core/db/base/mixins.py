from uuid import uuid4, UUID
from datetime import datetime
from sqlalchemy.orm import mapped_column, Mapped, relationship, declared_attr
from sqlalchemy import TIMESTAMP, ForeignKey
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


class SoftDeleteMixin:
    deleted_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=None, nullable=True
    )

    def delete(self) -> None:
        self.deleted_at = utc_now()

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None


class CreatedByMixin:
    created_by_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    @declared_attr
    def created_by(self) -> Mapped["User"]:  # type: ignore  # noqa
        return relationship("User", foreign_keys=self.created_by_user_id)  # type: ignore # noqa


class LastModifiedByMixin:
    last_modified_by_user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), nullable=True, default=None
    )

    @declared_attr
    def last_modified_by(self) -> Mapped["User"]:  # type: ignore # noqa
        return relationship("User", foreign_keys=self.last_modified_by_user_id)  # type: ignore # noqa


class TimestampMixin(CreatedAtMixin, UpdatedAtMixin): ...
