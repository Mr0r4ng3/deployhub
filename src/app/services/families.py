from typing import Sequence
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core.security.models.users import User
from app.models.families import Family
from app.schemas.families import FamilyCreateSchema
from app.pagination import paginate
from app.schemas.pagination import PaginationParams


class FamiliesService:
    """
    Service for managing Families.

    Args:
        db (Session): A database session.

    Attributes:
        _db (Session): Internal database session.
    """

    def __init__(self, db: Session) -> None:
        """
        Initialize the FamiliesService with a database session.

        Args:
            db (Session): A database session for interacting with the database.
        """
        self._db = db

    def list(self, pagination: PaginationParams) -> tuple[Sequence[Family], int]:
        """
        Retrieve a list of families.

        Args:
            skip (int, optional): Number of records to skip. Defaults to 0.
            limit (int, optional): Maximum number of records to retrieve. Defaults to 100.

        Returns:
            Sequence[Family]: A list of Family objects.
        """
        statement = (
            select(Family).where(Family.deleted_at == None)  # noqa: E711
        )

        return paginate(
            session=self._db,
            statement=statement,
            pagination=pagination,
        )

    def create(self, family_create: FamilyCreateSchema, user: User) -> Family:
        """
        Create a new family in the database.

        Args:
            new_family (FamilyCreate): The data required to create a new family.

        Returns:
            Family: The newly created Family object.
        """
        family = Family(created_by_user_id=user.id, **family_create.model_dump())
        self._db.add(family)
        self._db.commit()
        self._db.refresh(family)
        return family

    def get(self, family_id: int) -> Family | None:
        """
        Retrieve a family by its unique identifier.

        Args:
            family_id (int): The unique identifier of the family to retrieve.

        Returns:
            Family: The Family object corresponding to the given ID, or None if not found.
        """
        statement = (
            select(Family)
            .where(Family.id == family_id)
            .where(Family.deleted_at == None)  # noqa: E711
        )
        return self._db.scalars(statement).first()
