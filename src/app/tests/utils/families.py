from app.tests.conftest import get_session
from app.models.families import Family
from app.tests.utils.generic import random_lower_string


def create_random_family() -> Family:
    with get_session() as db:
        name = random_lower_string()

        family = Family(name=name)

        db.add(family)
        db.commit()
        db.refresh(family)

        return family
