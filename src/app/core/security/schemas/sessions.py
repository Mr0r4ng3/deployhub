from datetime import datetime
from uuid import UUID
from app.core.security.types import SessionCloseReason
from app.schemas.base import Schema


class UserSessionBaseSchema(Schema):
    user_id: int
    device_info: str
    location: str | None
    expires_at: datetime
    last_used_at: datetime
    is_active: bool
    close_reason: SessionCloseReason | None


class UserSessionSchema(UserSessionBaseSchema):
    id: UUID


class UserSessionPublicSchema(UserSessionSchema): ...
