from uuid import UUID
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyCookie
from app.core.db.dependencies import DbDep
from app.core.security.models.sessions import UserSession
from app.core.security.models.users import User
from app.core.security.services.sessions import UserSessionService

NotAuthenticated = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
)

CookieScheme = APIKeyCookie(name="session_id", auto_error=False)


def get_current_session(
    db: DbDep, session_id_cookie: str | None = Depends(CookieScheme)
) -> UserSession:
    if not session_id_cookie:
        raise NotAuthenticated

    try:
        id = UUID(session_id_cookie)

    except ValueError:
        raise NotAuthenticated

    service = UserSessionService(db)
    session = service.get_valid_session_by_id(id)

    if not session:
        raise NotAuthenticated

    service.update_last_used_at(session.id)

    return session


CurrentSessionDep = Annotated[UserSession, Depends(get_current_session)]
