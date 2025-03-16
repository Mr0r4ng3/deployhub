from app.schemas.base import Schema
from pydantic import Field
from app.schemas.mixins import (
    IntegerPrimaryKeyMixin,
    TimestampMixin,
    CreatedByMixin,
    LastModifiedByMixin,
)


class FamilySchema(Schema):
    name: str = Field(min_length=1, max_length=100)


class FamilyCreateSchema(FamilySchema): ...


class FamilyPublicSchema(FamilySchema, IntegerPrimaryKeyMixin): ...


class FamilyDBSchema(
    FamilySchema,
    IntegerPrimaryKeyMixin,
    TimestampMixin,
    CreatedByMixin,
    LastModifiedByMixin,
): ...
