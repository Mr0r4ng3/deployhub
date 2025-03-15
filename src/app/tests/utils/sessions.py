from datetime import timedelta
from uuid import UUID, uuid4

import pytest
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core.security.models.users import User
from app.core.timezone import utc_now
from app.core.security.models.sessions import UserSession
from app.core.config import settings


@pytest.fixture(scope="function")
def session_id(db: Session, test_user: User) -> UUID:
    statement = (
        select(UserSession)
        .where(UserSession.user_id == test_user.id)
        .where(UserSession.is_active == True)  # noqa: E712
    )

    session = db.scalars(statement).first()

    if session is not None:
        return session.id

    new_session = UserSession(
        id=uuid4(),
        user_id=test_user.id,
        device_info="test",
        location="test",
        expires_at=utc_now() + timedelta(minutes=settings.SESSION_EXPIRE_MINUTES),
        last_used_at=utc_now(),
        is_active=True,
    )

    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    return new_session.id
