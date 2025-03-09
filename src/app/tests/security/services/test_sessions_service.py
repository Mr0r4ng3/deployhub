from datetime import timedelta
from uuid import UUID

from sqlmodel import Session

from app.core.security.services.sessions import UserSessionService
from app.core.security.types import SessionCloseReason
from app.core.timezone import utc_now
from app.tests.utils.sessions import create_session
from app.tests.utils.users import create_test_user
from app.core.config import settings


def test_user_session_service_get_by_id(db: Session) -> None:
    user = create_test_user()
    session_id = create_session(user.id)

    session_service = UserSessionService(db)
    session = session_service.get_by_id(session_id)

    assert session is not None
    assert session.id == session_id
    assert session.user_id == user.id


def test_user_session_service_get_by_id_non_existent(db: Session) -> None:
    session_service = UserSessionService(db)
    session = session_service.get_by_id(UUID(int=1))

    assert session is None


def test_user_session_service_create(db: Session) -> None:
    user = create_test_user()

    session_service = UserSessionService(db)
    session = session_service.create(user.id, "test", "127.0.0.1")

    assert session is not None
    assert session.id is not None
    assert session.user_id == user.id
    assert session.expires_at is not None
    assert session.last_used_at is not None


def test_user_session_service_update_last_used_at(db: Session) -> None:
    user = create_test_user()
    session_id = create_session(user.id)

    session_service = UserSessionService(db)

    previous_last_used_at = session_service.get_by_id(session_id).last_used_at

    session_service.update_last_used_at(session_id)

    session = session_service.get_by_id(session_id)

    assert session is not None
    assert session.last_used_at is not None
    assert session.last_used_at > previous_last_used_at


def test_user_session_service_get_valid_session_by_id(db: Session) -> None:
    user = create_test_user()
    session_id = create_session(user.id)

    session_service = UserSessionService(db)
    session = session_service.get_valid_session_by_id(session_id)

    assert session is not None
    assert session.id == session_id
    assert session.user_id == user.id
    assert session.is_active is True


def test_user_session_service_get_valid_session_by_id_non_existent(db: Session) -> None:
    session_service = UserSessionService(db)
    session = session_service.get_valid_session_by_id(UUID(int=1))

    assert session is None


def test_user_session_service_get_valid_session_by_id_inactive(db: Session) -> None:
    user = create_test_user()
    session_id = create_session(user.id)

    session_service = UserSessionService(db)
    session_service.invalidate_session(session_id, SessionCloseReason.UserRequest)

    session = session_service.get_valid_session_by_id(session_id)

    assert session is None


def test_user_session_service_get_valid_session_by_id_expired(db: Session) -> None:
    user = create_test_user()
    session_id = create_session(user.id)

    session_service = UserSessionService(db)
    session = session_service.get_by_id(session_id)

    assert session is not None

    session.expires_at = utc_now() - timedelta(minutes=1)
    session_service._db.add(session)
    session_service._db.commit()

    session = session_service.get_valid_session_by_id(session_id)

    assert session is None


def test_user_session_service_get_valid_session_by_id_user_inactive(
    db: Session,
) -> None:
    user = create_test_user()
    session_id = create_session(user.id)

    session_service = UserSessionService(db)
    session = session_service.get_by_id(session_id)

    assert session is not None

    session.last_used_at = utc_now() - timedelta(
        minutes=settings.INACTIVE_SESSION_MINUTES + 1
    )

    session_service._db.add(session)
    session_service._db.commit()

    session = session_service.get_valid_session_by_id(session_id)

    assert session is None
