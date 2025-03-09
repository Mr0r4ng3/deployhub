from fastapi.testclient import TestClient

from app.tests.utils.auth import login
from app.tests.utils.users import create_test_user


def test_login_success(client: TestClient) -> None:
    password = "testpass"
    user = create_test_user(password=password)

    response = client.post(
        "/login",
        json={"username": user.username, "password": password},
    )

    assert response.status_code == 200
    assert response.json()["username"] == user.username
    assert "session_id" in response.cookies


def test_login_invalid_credentials(client: TestClient) -> None:
    response = client.post(
        "/login",
        json={"username": "invalid", "password": "invalid"},
    )

    assert response.status_code == 403


def test_logout_success(client: TestClient) -> None:
    login(client)

    response = client.post("/logout")

    assert response.status_code == 200
    assert response.cookies.get("session_id") is None
