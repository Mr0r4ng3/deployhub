from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_create_family():
    response = client.post("/families/", json={"name": "test_family"})
    assert response.status_code == 200


def test_read_families():
    response = client.get("/families/")
    assert response.status_code == 200
