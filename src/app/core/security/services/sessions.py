from uuid import UUID
from user_agents import parse  # type: ignore
from datetime import timedelta
from sqlalchemy.orm import Session
from app.core.security.types import SessionCloseReason
from app.core.security.models.sessions import UserSession
from app.core.security.schemas.sessions import UserSessionPublicSchema
from app.core.config import settings
from app.core.timezone import utc_now


class UserSessionService:
    """
    Service for managing UserSessions.

    Args:
        db (Session): A database session.

    Attributes:
        _db (Session): Internal database session.
    """

    def __init__(self, db: Session):
        """
        Initialize the service with a database session.

        Args:
            db (Session): A database session.
        """
        self._db = db

    def create(
        self, user_id: int, user_agent: str | None, ip_address: str | None = None
    ) -> UserSessionPublicSchema:
        """
        Create a new UserSession.

        Args:
            user_id (int): ID of the user.
            user_agent (str): User agent string from the client's request.
            ip_address (str | None): IP address of the client, if available.

        Returns:
            UserSessionPublic: The newly created user session.
        """
        device_info = self._parse_device(user_agent) if user_agent else "Unknown"
        location = self._get_location(ip_address) if ip_address else "Unknown"
        expires_at = utc_now() + timedelta(minutes=settings.SESSION_EXPIRE_MINUTES)

        new_session = UserSession(
            user_id=user_id,
            device_info=device_info,
            location=location,
            expires_at=expires_at,
            last_used_at=utc_now(),
        )

        self._db.add(new_session)
        self._db.commit()
        self._db.refresh(new_session)

        return UserSessionPublicSchema(
            id=new_session.id,
            user_id=new_session.user_id,
            device_info=new_session.device_info,
            location=new_session.location,
            expires_at=new_session.expires_at,
            last_used_at=new_session.last_used_at,
            is_active=new_session.is_active,
            close_reason=new_session.close_reason,
        )

    def get(self, id: UUID) -> UserSession | None:
        """
        Retrieve a UserSession by its ID.

        Args:
            id (UUID): The unique identifier of the session.

        Returns:
            UserSession | None: The session if found, otherwise None.
        """
        return self._db.get(UserSession, id)

    def get_valid_session(self, id: UUID) -> UserSession | None:
        """
        Retrieve a valid UserSession by its ID, invalidating it if expired or inactive.

        Args:
            id (UUID): The unique identifier of the session.

        Returns:
            UserSession | None: The valid session if found, otherwise None.
        """
        session = self.get(id)

        if not session or not session.is_active:
            return None

        if session.is_expired:
            self.invalidate_session(session.id, SessionCloseReason.Expired)
            return None

        if session.is_inactivity_limit_reached:
            self.invalidate_session(id, SessionCloseReason.Inactivity)
            return None

        return session

    def invalidate_session(self, id: UUID, reason: SessionCloseReason) -> None:
        """
        Invalidate a UserSession and set the close reason.

        Args:
            id (UUID): The unique identifier of the session.
            reason (SessionCloseReason): The reason for invalidating the session.
        """
        session = self._db.get(UserSession, id)

        if session:
            session.is_active = False
            session.close_reason = reason
            self._db.add(session)
            self._db.commit()

    def update_last_used_at(self, id: UUID) -> None:
        """
        Update the last_used_at field of a UserSession.

        Args:
            id (UUID): The unique identifier of the session.
        """
        session = self._db.get(UserSession, id)

        if session:
            session.last_used_at = utc_now()
            self._db.add(session)
            self._db.commit()

    def _parse_device(self, user_agent: str) -> str:
        """
        Parse the user agent string to extract device information.

        Args:
            user_agent (str): The user agent string.

        Returns:
            str: A formatted string containing device and browser information.
        """
        parsed_user_agent = parse(user_agent)
        return f"{parsed_user_agent.device.family} {parsed_user_agent.browser.family} ({parsed_user_agent.os.family})"

    def _get_location(self, ip_address: str | None) -> str | None:
        """
        Get the geographical location from the IP address. (Placeholder for actual implementation)

        Args:
            ip_address (str | None): The IP address.

        Returns:
            str | None: The location as a string, or None if not available.
        """
        # TODO: Implement location fetching logic here
        pass
