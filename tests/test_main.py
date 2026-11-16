from fastapi.testclient import TestClient

from main import app, url_database

client = TestClient(app)


def test_home_returns_200_json():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Smart URL Shortener is running"


def test_health_reports_uptime_and_ready():
    response = client.get("/health")
    body = response.json()
    assert response.status_code == 200
    assert body["status"] == "healthy"
    assert body["ready"] is True
    assert body["uptime_seconds"] >= 0


def test_shorten_and_redirect():
    response = client.post("/shorten", json={"url": "https://example.com/page"})
    assert response.status_code == 200
    code = response.json()["short_code"]
    assert len(code) == 6
    assert code in url_database

    redirect = client.get(f"/{code}", follow_redirects=False)
    assert redirect.status_code in (302, 307)
    assert redirect.headers["location"] == "https://example.com/page"


def test_unknown_code_returns_404():
    response = client.get("/doesnotexist")
    assert response.status_code == 404


def test_invalid_url_rejected():
    response = client.post("/shorten", json={"url": "not-a-url"})
    assert response.status_code == 422
