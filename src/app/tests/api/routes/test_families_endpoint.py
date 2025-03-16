from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.sql.functions import func
from app.core.security.models.users import User
from app.models.families import Family
from app.schemas.families import FamilyCreateSchema, FamilyPublicSchema
from app.core.config import settings
from app.tests.utils.families import create_random_family
from app.tests.utils.generic import random_lower_string

BASE_URL = f"{settings.API_V1_STR}/families/"


def test_create_family_unauthorized(
    client: TestClient,
):
    new_family = FamilyCreateSchema(name=random_lower_string(10))

    response = client.post(BASE_URL, json=new_family.model_dump())

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_family(logged_client: TestClient):
    new_family = FamilyCreateSchema(name=random_lower_string(10))

    response = logged_client.post(BASE_URL, json=new_family.model_dump())

    assert response.status_code == status.HTTP_201_CREATED
    content = response.json()
    assert content["name"] == new_family.name


def test_create_family_name_too_long(logged_client: TestClient):
    response = logged_client.post(BASE_URL, json={"name": random_lower_string(101)})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_family_name_missing(
    logged_client: TestClient,
):
    response = logged_client.post(BASE_URL, json={})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_read_family_by_id_unauthorized(client: TestClient, random_family):
    response = client.get(f"{BASE_URL}{random_family.id}")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_read_family_by_id(logged_client: TestClient, random_family):
    expected_family = FamilyPublicSchema.model_validate(random_family)

    response = logged_client.get(f"{BASE_URL}{random_family.id}")

    assert response.status_code == status.HTTP_200_OK
    content = FamilyPublicSchema.model_validate(response.json())

    assert content == expected_family


def test_read_family_by_id_not_found(logged_client: TestClient, db: Session):
    id = db.scalars(select(func.max(Family.id))).first() or 0

    response = logged_client.get(f"{BASE_URL}{id + 1}")

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_read_families_unauthorized(
    client: TestClient,
):
    response = client.get(BASE_URL)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_read_families(logged_client: TestClient, db: Session, test_user: User):
    for _ in range(5):
        create_random_family(db, test_user)

    response = logged_client.get(BASE_URL)

    assert response.status_code == 200
    content = response.json()
    assert len(content["items"]) >= 5
    assert content["pagination"]
    assert content["pagination"]["total_count"]
    assert content["pagination"]["max_page"]
