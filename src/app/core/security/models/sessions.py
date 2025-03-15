from app.core.security.types import SessionCloseReason
from datetime import datetime, timedelta
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import TIMESTAMP, ForeignKey, String
from app.core.db.base.mixins import (
    CreatedAtMixin,
    UUIDPrimaryKeyMixin,
)
from app.core.db.base.models import Model
from app.core.timezone import utc_now
from app.core.config import settings


class UserSession(Model, CreatedAtMixin, UUIDPrimaryKeyMixin):
    __tablename__ = "user_sessions"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    device_info: Mapped[str]
    location: Mapped[str | None]

    expires_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )

    last_used_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )

    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    close_reason: Mapped[SessionCloseReason | None] = mapped_column(
        nullable=True, default=None
    )

    user: Mapped["User"] = relationship(back_populates="sessions")  # type: ignore # noqa: F821

    @property
    def is_expired(self) -> bool:
        return self.expires_at < utc_now()

    @property
    def is_inactivity_limit_reached(self) -> bool:
        return self.last_used_at < utc_now() - timedelta(
            minutes=settings.INACTIVE_SESSION_MINUTES
        )
