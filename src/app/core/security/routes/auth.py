from fastapi import Request, Response, status
from fastapi.routing import APIRouter
from app.core.db.depends import DbDep
from app.core.security.depends import CurrentSessionDep
from app.core.security.schemas.auth import LoginSchema
from app.core.security.schemas.users import UserPublicSchema
from app.core.security.services.auth import AuthService
from app.core.security.services.sessions import UserSessionService
from app.core.config import settings
from app.core.security.types import SessionCloseReason
from app.exceptions import InvalidCredentials


router = APIRouter(
    tags=["auth"],
)


@router.post(
    "/login",
    response_model=UserPublicSchema,
    status_code=status.HTTP_200_OK,
    responses={401: {"description": "Invalid credentials"}},
)
def login(request: Request, response: Response, db: DbDep, login_data: LoginSchema):
    auth_service = AuthService(db)

    user = auth_service.authenticate_user(login_data.username, login_data.password)

    if not user:
        raise InvalidCredentials()

    session_service = UserSessionService(db)

    user_agent = request.headers.get("User-Agent")
    ip_address = request.client.host if request.client else None

    session = session_service.create(user.id, user_agent, ip_address)

    response.set_cookie(
        key="session_id",
        value=str(session.id),
        httponly=settings.COOKIE_HTTP_ONLY,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        max_age=settings.SESSION_EXPIRE_MINUTES * 60,  # in seconds
    )

    return UserPublicSchema(
        id=user.id,
        username=user.username,
        name=user.name,
        surname=user.surname,
    )


@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(response: Response, current_session: CurrentSessionDep, db: DbDep) -> None:
    session_service = UserSessionService(db)

    session_service.invalidate_session(current_session.id, SessionCloseReason.Logout)

    response.delete_cookie(key="session_id")
