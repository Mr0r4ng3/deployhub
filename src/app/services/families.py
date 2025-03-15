from typing import Sequence
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.families import Family
from app.schemas.families import FamilyCreateSchema


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

    def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[Family]:
        """
        Retrieve a list of families.

        Args:
            skip (int, optional): Number of records to skip. Defaults to 0.
            limit (int, optional): Maximum number of records to retrieve. Defaults to 100.

        Returns:
            Sequence[Family]: A list of Family objects.
        """
        statement = (
            select(Family).where(Family.deleted_at == None).offset(skip).limit(limit)  # noqa: E711
        )
        return self._db.scalars(statement).all()

    def create(self, new_family: FamilyCreateSchema) -> Family:
        """
        Create a new family in the database.

        Args:
            new_family (FamilyCreate): The data required to create a new family.

        Returns:
            Family: The newly created Family object.
        """
        family = Family(name=new_family.name)
        self._db.add(family)
        self._db.commit()
        self._db.refresh(family)
        return family

    def get_by_id(self, family_id: int) -> Family | None:
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
