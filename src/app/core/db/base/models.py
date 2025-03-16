from sqlalchemy.orm import DeclarativeBase
from .mixins import (
    IntegerPrimaryKeyMixin,
    TimestampMixin,
    SoftDeleteMixin,
    CreatedByMixin,
    LastModifiedByMixin,
)


class Model(DeclarativeBase):
    __abstract__ = True


class RecordModel(
    Model,
    IntegerPrimaryKeyMixin,
    TimestampMixin,
    SoftDeleteMixin,
):
    __abstract__ = True


class MonitoredModel(RecordModel, CreatedByMixin, LastModifiedByMixin):
    __abstract__ = True
