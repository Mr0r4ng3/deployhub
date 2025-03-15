from fastapi.testclient import TestClient


def test_login_success(logged_client: TestClient, test_user) -> None:
    password = "testpass"

    response = logged_client.post(
        "/login",
        json={"username": test_user.username, "password": password},
    )

    assert response.status_code == 200
    assert response.json()["username"] == test_user.username
    assert "session_id" in response.cookies


def test_login_invalid_credentials(logged_client: TestClient) -> None:
    response = logged_client.post(
        "/login",
        json={"username": "invalid", "password": "invalid"},
    )

    assert response.status_code == 401


def test_logout_success(logged_client: TestClient) -> None:
    response = logged_client.post("/logout")

    assert response.status_code == 200
    assert response.cookies.get("session_id") is None
