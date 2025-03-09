from sqlmodel import Session, select

from app.core.security.models.users import User, UserCreate, UserPublic
from app.core.security.func import get_hash_password


class UserService:
    """
    Service for managing users

    Args:
        db (Session): A database session.

    Attributes:
        _db (Session): Internal database session.
    """

    def __init__(self, db: Session):
        """
        Initialize the UserService with a database session.

        Args:
            db (Session): A database session
        """
        self._db = db

    def create(self, user: UserCreate) -> UserPublic:
        """
        Creates a new user and returns it

        Args:
            user (UserCreate): The user to create

        Returns:
            UserPublic: The created user
        """
        hashed_password = get_hash_password(user.password)
        new_user = User(
            username=user.username,
            name=user.name,
            surname=user.surname,
            hashed_password=hashed_password,
        )

        self._db.add(new_user)
        self._db.commit()
        self._db.refresh(new_user)
        return UserPublic.model_validate(new_user)

    def get_by_username(self, username: str) -> User | None:
        """
        Retrieves a user by username

        Args:
            username (str): The username of the user to retrieve

        Returns:
            User | None: The user if found, or None otherwise
        """
        statement = select(User).where(User.username == username)
        return self._db.exec(statement).first()
