from sqlmodel import Session
from app.core.security.models.users import User
from app.core.security.func import verify_password
from app.core.security.services.user import UserService


class AuthService:
    """
    Service for authenticating users

    Args:
        db (Session): A database session.

    Attributes:
        _db (Session): Internal database session.
    """

    def __init__(self, db: Session):
        """
        Initialize the AuthService with a database session.

        Args:
            db (Session): A database session
        """
        self._db = db

    def authenticate_user(self, username: str, password: str) -> User | None:
        """
        Authenticates a user by username and password

        Args:
            username (str): The username of the user
            password (str): The password of the user

        Returns:
            User | None: The user object if the authentication is successful,
                or None otherwise
        """
        user_service = UserService(self._db)

        user = user_service.get_by_username(username)

        if user and verify_password(password, user.hashed_password):
            return user

        return None
