from fastapi.testclient import TestClient

from app import create_mock_app


def test_health():
    client = TestClient(create_mock_app())
    response = client.get("/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
