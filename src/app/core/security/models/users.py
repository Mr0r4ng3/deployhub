from sqlmodel import Field, Relationship
from app.core.db.base.models import RecordModel, Base


class UserBase(Base):
    name: str = Field(max_length=100)
    surname: str | None = Field(default=None, max_length=100, nullable=True)
    username: str = Field(index=True, max_length=100, unique=True)


class User(UserBase, RecordModel, table=True):
    hashed_password: str = Field()
    sessions: list["UserSession"] = Relationship(back_populates="user")  # type: ignore # noqa


class UserCreate(UserBase):
    password: str


class UserPublic(UserBase, RecordModel): ...
