from datetime import datetime
from uuid import UUID


class UUIDPrimaryKeyMixin:
    id: UUID


class IntegerPrimaryKeyMixin:
    id: int


class CreatedAtMixin:
    created_at: datetime


class UpdatedAtMixin:
    updated_at: datetime


class DeletedAtMixin:
    deleted_at: datetime


class CreatedByMixin:
    created_by_user_id: int


class LastModifiedByMixin:
    last_modified_by_user_id: int | None = None


class TimestampMixin(CreatedAtMixin, UpdatedAtMixin): ...
