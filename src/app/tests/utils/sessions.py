from datetime import timedelta
from uuid import UUID, uuid4
from app.core.timezone import utc_now
from app.tests.conftest import get_session
from app.core.security.models.sessions import UserSession
from app.core.config import settings


def create_session(user_id: int) -> UUID:
    with get_session() as db:
        session = UserSession(
            id=uuid4(),
            user_id=user_id,
            device_info="test",
            location="test",
            expires_at=utc_now() + timedelta(minutes=settings.SESSION_EXPIRE_MINUTES),
            last_used_at=utc_now(),
            is_active=True,
        )

        db.add(session)
        db.commit()
        db.refresh(session)

        return session.id
