from datetime import timedelta
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.security.services.sessions import UserSessionService
from app.core.security.types import SessionCloseReason
from app.core.timezone import utc_now
from app.core.config import settings


def test_user_session_service_get_by_id(db: Session, test_user, session_id) -> None:
    session_service = UserSessionService(db)
    session = session_service.get(session_id)

    assert session is not None
    assert session.id == session_id
    assert session.user_id == test_user.id


def test_user_session_service_get_by_id_non_existent(db: Session) -> None:
    session_service = UserSessionService(db)
    session = session_service.get(UUID(int=1))

    assert session is None


def test_user_session_service_create(db: Session, test_user) -> None:
    session_service = UserSessionService(db)
    session = session_service.create(test_user.id, "test", "127.0.0.1")

    assert session is not None
    assert session.id is not None
    assert session.user_id == test_user.id
    assert session.expires_at is not None
    assert session.last_used_at is not None


def test_user_session_service_update_last_used_at(db: Session, session_id) -> None:
    session_service = UserSessionService(db)

    previus_session = session_service.get(session_id)

    assert previus_session is not None

    previus_last_used_at = previus_session.last_used_at

    session_service.update_last_used_at(session_id)

    session = session_service.get(session_id)

    assert session is not None
    assert session.last_used_at is not None
    assert session.last_used_at > previus_last_used_at


def test_user_session_service_get_valid_session_by_id(
    db: Session, test_user, session_id
) -> None:
    session_service = UserSessionService(db)
    session = session_service.get_valid_session(session_id)

    assert session is not None
    assert session.id == session_id
    assert session.user_id == test_user.id
    assert session.is_active is True


def test_user_session_service_get_valid_session_by_id_non_existent(db: Session) -> None:
    session_service = UserSessionService(db)
    session = session_service.get_valid_session(UUID(int=1))

    assert session is None


def test_user_session_service_get_valid_session_by_id_inactive(
    db: Session, session_id
) -> None:
    session_service = UserSessionService(db)
    session_service.invalidate_session(session_id, SessionCloseReason.UserRequest)

    session = session_service.get_valid_session(session_id)

    assert session is None


def test_user_session_service_get_valid_session_by_id_expired(
    db: Session, session_id
) -> None:
    session_service = UserSessionService(db)
    session = session_service.get(session_id)

    assert session is not None

    session.expires_at = utc_now() - timedelta(minutes=1)
    session_service._db.add(session)
    session_service._db.commit()

    session = session_service.get_valid_session(session_id)

    assert session is None


def test_user_session_service_get_valid_session_by_id_user_inactive(
    db: Session, session_id
) -> None:
    session_service = UserSessionService(db)
    session = session_service.get(session_id)

    assert session is not None

    session.last_used_at = utc_now() - timedelta(
        minutes=settings.INACTIVE_SESSION_MINUTES + 1
    )

    session_service._db.add(session)
    session_service._db.commit()

    session = session_service.get_valid_session(session_id)

    assert session is None
