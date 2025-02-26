from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session, select
from sqlalchemy.sql.functions import func
from app.models.families import FamilyCreate, FamilyPublic, Family
from app.core.config import settings
from app.tests.utils.families import create_random_family
from app.tests.utils.generic import random_lower_string

BASE_URL = f"{settings.API_V1_STR}/families/"


def test_create_family(client: TestClient):
    new_family = FamilyCreate(name=random_lower_string(10))

    response = client.post(BASE_URL, json=new_family.model_dump())

    assert response.status_code == status.HTTP_201_CREATED
    content = response.json()
    assert content["name"] == new_family.name


def test_create_family_name_too_long(client: TestClient):
    response = client.post(BASE_URL, json={"name": random_lower_string(101)})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_family_name_missing(client: TestClient):
    response = client.post(BASE_URL, json={})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_read_family_by_id(client: TestClient, db: Session):
    family = create_random_family(db=db)
    expected_family = FamilyPublic.model_validate(family)

    response = client.get(f"{BASE_URL}{family.id}")

    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content == expected_family.model_dump()


def test_read_family_by_id_not_found(client: TestClient, db: Session):
    id = db.exec(select(func.max(Family.id))).first()

    response = client.get(f"{BASE_URL}{id + 1}")

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_read_families(client: TestClient, db: Session):
    for _ in range(5):
        create_random_family(db)

    response = client.get(BASE_URL)

    assert response.status_code == 200
    content = response.json()
    assert len(content) >= 5
