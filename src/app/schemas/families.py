from app.schemas.base import Schema
from pydantic import Field


class FamilySchema(Schema):
    name: str = Field(min_length=1, max_length=100)


class FamilyCreateSchema(FamilySchema):
    pass


class FamilyPublicSchema(FamilySchema):
    id: int
