from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine

from app.core.db.base.models import SQLModel
from app.models import *  # noqa
from app.core.db.database import get_db
from app.core.config import settings
from app.main import app

engine = create_engine(settings.TEST_DATABASE_URI)


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    SQLModel.metadata.create_all(engine)  # noqa

    with Session(engine) as session:
        yield session


@pytest.fixture(scope="module")
def client(db) -> Generator[TestClient, None, None]:
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c
