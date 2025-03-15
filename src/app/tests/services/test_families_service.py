from sqlalchemy.orm import Session
from app.schemas.pagination import PaginationParams
from app.services.families import FamiliesService
from app.schemas.families import FamilyCreateSchema
from app.tests.utils.generic import random_lower_string
from app.tests.utils.families import create_random_family


def test_create_family(db: Session):
    name = random_lower_string()
    service = FamiliesService(db)

    family = service.create(FamilyCreateSchema(name=name))

    assert family.name == name
    assert family.id is not None


def test_get_family(db: Session, random_family):
    service = FamiliesService(db)

    fetched_family = service.get(random_family.id)

    assert fetched_family == random_family


def test_get_families(db: Session):
    for _ in range(5):
        create_random_family(db)

    pagination = PaginationParams(page=1, limit=5)

    service = FamiliesService(db)

    result, count = service.list(pagination)

    assert len(result) == 5
    assert count >= 5
