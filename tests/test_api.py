from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_shorten_url():
    response = client.post(
        "/shorten",
        json={"url": "https://www.google.com"}
    )

    assert response.status_code == 200
    assert "short_code" in response.json()
    assert "short_url" in response.json()


def test_invalid_short_url():
    response = client.get("/doesnotexist")

    assert response.status_code == 404