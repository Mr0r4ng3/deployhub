from sqlmodel import Field
from app.core.db.base.models import RecordModel, Base


class FamilyBase(Base):
    name: str = Field(index=True, max_length=100, unique=True)


class FamilyCreate(FamilyBase):
    pass


class Family(FamilyBase, RecordModel, table=True): ...


class FamilyPublic(Family, table=False): ...
