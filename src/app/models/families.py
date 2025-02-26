from sqlmodel import Field
from app.models import SQLModel


class FamilyBase(SQLModel):
    name: str = Field(index=True, max_length=100)


class FamilyCreate(FamilyBase):
    pass


class Family(FamilyBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class FamilyPublic(FamilyBase):
    id: int
