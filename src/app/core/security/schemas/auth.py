from app.schemas.base import Schema


class LoginSchema(Schema):
    username: str
    password: str
