import pytest
from app.models.families import Family
from app.tests.utils.generic import random_lower_string


@pytest.fixture(scope="function")
def random_family(db) -> Family:
    return create_random_family(db)


def create_random_family(db) -> Family:
    name = random_lower_string()

    family = Family(name=name)

    db.add(family)
    db.commit()
    db.refresh(family)

    return family
