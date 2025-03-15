from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from app.core.db.base.models import Model
from app.models import *  # noqa
from app.core.security.models import *  # noqa
from app.core.db.database import get_db
from app.core.config import settings
from app.main import app
from app.tests.utils import *  # noqa: F403


@pytest.fixture(scope="session")
def db_engine(request):
    engine = create_engine(settings.TEST_DATABASE_URI)

    Model.metadata.create_all(engine)

    yield engine

    engine.dispose()


@pytest.fixture(scope="session")
def db_session_factory(db_engine):
    return scoped_session(sessionmaker(bind=db_engine))


@pytest.fixture(scope="function")
def db(db_session_factory):
    session = db_session_factory()

    yield session

    session.rollback()
    session.close()


@pytest.fixture(scope="function")
def client(db) -> Generator[TestClient, None, None]:
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c
