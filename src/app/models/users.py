from sqlmodel import Field
from app.core.db.base.models import RecordModel, Base


class UserBase(Base):
    name: str = Field(max_length=100)
    surname: str = Field(max_length=100, nullable=True)
    username: str = Field(index=True, max_length=100, unique=True)


class User(UserBase, RecordModel, table=True):
    hashed_password: str = Field()


class UserCreate(UserBase):
    password: str


class UserPublic(UserBase, RecordModel): ...
