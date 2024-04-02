from fastapi.testclient import TestClient

from app import create_mock_app


def test_login_mongomock():
    client = TestClient(create_mock_app())
    response = client.post("/v1/auth/login")
    assert response.status_code == 200
    assert response.json() == {"message": "Login Successfully!"}
