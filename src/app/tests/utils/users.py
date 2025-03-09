from sqlmodel import select
from app.core.security.func import get_hash_password
from app.tests.conftest import get_session
from app.core.security.models.users import User


def create_test_user(username: str = "testuser", password: str = "testpass") -> User:
    with get_session() as db:
        statement = select(User).where(User.username == username)

        user = db.exec(statement).first()

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
