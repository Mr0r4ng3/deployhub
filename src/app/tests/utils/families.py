import pytest
from app.core.security.models.users import User
from app.models.families import Family
from app.tests.utils.generic import random_lower_string


@pytest.fixture(scope="function")
def random_family(db, test_user: User) -> Family:
    return create_random_family(db, test_user)


def create_random_family(db, test_user: User) -> Family:
    name = random_lower_string()

    family = Family(name=name, created_by_user_id=test_user.id)

    db.add(family)
    db.commit()
    db.refresh(family)

    return family
