from sqlmodel import Session
from app.models.families import FamilyCreate, Family
from app.tests.utils.generic import random_lower_string
from app.services.families import FamiliesService


def create_random_family(db: Session) -> Family:
    name = random_lower_string()

    new_family = FamilyCreate(name=name)

    service = FamiliesService(db)

    family = service.create(new_family)

    return family
