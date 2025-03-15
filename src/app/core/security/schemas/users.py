from app.schemas.base import Schema


class UserBaseSchema(Schema):
    username: str
    name: str
    surname: str | None = None


class UserSchema(UserBaseSchema):
    id: int


class UserCreateSchema(UserBaseSchema):
    password: str


class UserPublicSchema(UserSchema): ...
