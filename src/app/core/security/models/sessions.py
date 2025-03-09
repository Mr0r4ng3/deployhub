from app.core.security.types import SessionCloseReason
from datetime import datetime, timedelta
from sqlmodel import Field, Relationship, Column, Enum, DateTime
from app.core.db.base.mixins import (
    CreatedAtMixin,
    UUIDPrimaryKeyMixin,
)
from app.core.db.base.models import Base
from app.core.security.models.users import User
from app.core.timezone import utc_now
from app.core.config import settings


class UserSessionBase(Base, CreatedAtMixin, UUIDPrimaryKeyMixin):
    user_id: int = Field(foreign_key="user.id")
    device_info: str
    location: str | None

    expires_at: datetime = Field(sa_type=DateTime(timezone=True), nullable=False)

    last_used_at: datetime = Field(sa_type=DateTime(timezone=True), nullable=False)

    is_active: bool = Field(default=True, nullable=False)

    close_reason: SessionCloseReason | None = Field(
        sa_column=Column(Enum(SessionCloseReason), nullable=True, default=None)
    )

    @property
    def is_expired(self) -> bool:
        return self.expires_at < utc_now()

    @property
    def is_inactivity_limit_reached(self) -> bool:
        return self.last_used_at < utc_now() - timedelta(
            minutes=settings.INACTIVE_SESSION_MINUTES
        )


class UserSession(UserSessionBase, table=True):
    user: User = Relationship(back_populates="sessions")


class UserSessionPublic(UserSessionBase): ...
