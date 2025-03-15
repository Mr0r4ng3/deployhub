import pytest
from sqlalchemy import select
from app.core.security.func import get_hash_password
from app.core.security.models.users import User


@pytest.fixture(scope="function")
def test_user(db, username: str = "testuser", password: str = "testpass") -> User:
    statement = select(User).where(User.username == username)

    user = db.scalars(statement).first()

    if not user:
        user = User(
            username=username,
            name="Test",
            surname="User",
            hashed_password=get_hash_password(password),
        )

        db.add(user)
        db.commit()
        db.refresh(user)

    return user
