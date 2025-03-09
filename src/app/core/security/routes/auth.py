from fastapi import HTTPException, Request, Response, status
from fastapi.routing import APIRouter
from app.core.db.dependencies import DbDep
from app.core.security.dependencies import CurrentSessionDep
from app.core.security.models.auth import LoginData
from app.core.security.models.users import UserPublic
from app.core.security.services.auth import AuthService
from app.core.security.services.sessions import UserSessionService
from app.core.config import settings
from app.core.security.types import SessionCloseReason

router = APIRouter(
    tags=["auth"],
)

InvalidCredentials = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
)


@router.post("/login", response_model=UserPublic, status_code=status.HTTP_200_OK)
def login(request: Request, response: Response, db: DbDep, login_data: LoginData):
    auth_service = AuthService(db)

    user = auth_service.authenticate_user(login_data.username, login_data.password)

    if not user:
        raise InvalidCredentials

    session_service = UserSessionService(db)

    user_agent = request.headers.get("User-Agent")
    ip_address = request.client.host

    session = session_service.create(user.id, user_agent, ip_address)

    response.set_cookie(
        key="session_id",
        value=str(session.id),
        httponly=settings.COOKIE_HTTP_ONLY,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        max_age=settings.SESSION_EXPIRE_MINUTES * 60,  # in seconds
    )

    return UserPublic.model_validate(user)


@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(response: Response, current_session: CurrentSessionDep, db: DbDep) -> None:
    session_service = UserSessionService(db)

    session_service.invalidate_session(current_session.id, SessionCloseReason.Logout)

    response.delete_cookie(key="session_id")
