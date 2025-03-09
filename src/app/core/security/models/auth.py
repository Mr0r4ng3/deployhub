from sqlmodel import SQLModel


class LoginData(SQLModel):
    username: str
    password: str
