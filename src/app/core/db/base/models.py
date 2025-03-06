from sqlmodel import SQLModel
from .mixins import IntegerPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin


class Base(SQLModel): ...


class RecordModel(Base, IntegerPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin): ...
