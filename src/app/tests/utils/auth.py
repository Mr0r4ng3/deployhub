import pytest
from uuid import UUID
from fastapi.testclient import TestClient


@pytest.fixture(scope="function")
def logged_client(client: TestClient, session_id: UUID) -> TestClient:
    client.cookies["session_id"] = str(session_id)

    return client
