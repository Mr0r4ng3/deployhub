from typing import Sequence
from sqlmodel import Session, select
from app.models.families import FamilyCreate, Family


class FamiliesService:
    def __init__(self, db: Session):
        self._db = db

    def get_all(self, skip: int, limit: int) -> Sequence[Family]:
        statement = (
            select(Family).where(Family.deleted_at == None).offset(skip).limit(limit)  # noqa: E711
        )

        return self._db.exec(statement=statement).all()

    def create(self, new_family: FamilyCreate) -> Family:
        family = Family.model_validate(new_family)

        self._db.add(instance=family)
        self._db.commit()
        self._db.refresh(family)

        return family

    def get_by_id(self, family_id: int) -> Family:
        statement = (
            select(Family)
            .where(Family.id == family_id)
            .where(Family.deleted_at == None)  # noqa: E711
        )

        return self._db.exec(statement=statement).first()
