from fastapi.testclient import TestClient
from app.tests.utils.users import create_test_user
from app.tests.utils.sessions import create_session


def login(client: TestClient) -> None:
    user = create_test_user()

    session_id = create_session(user_id=user.id)

    client.cookies["session_id"] = str(session_id)
