import os

# The test suite must never connect to a configured production database.
os.environ["DATABASE_URL"] = "sqlite:///./test_stramos.db"
os.environ["ADMIN_API_TOKEN"] = "test-admin-token"

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.settings import settings


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_health_and_public_read_routes(client):
    assert client.get("/health").status_code == 200
    assert client.get("/api/contact").status_code == 200
    assert client.get("/api/programs").status_code == 200
    assert client.get("/api/events").status_code == 200


def test_unknown_event_is_not_found(client):
    response = client.get("/api/events/does-not-exist")
    assert response.status_code == 404


def test_private_lists_require_admin_token(client):
    for path in (
        "/api/volunteers",
        "/api/partners",
        "/api/donations",
        "/api/outreach-reports",
    ):
        assert client.get(path).status_code == 401
        assert client.get(path, headers={"X-Admin-Token": "wrong"}).status_code == 401
        assert client.get(path, headers={"X-Admin-Token": "test-admin-token"}).status_code == 200


def test_private_lists_fail_closed_without_configured_token(client, monkeypatch):
    monkeypatch.setattr(settings, "admin_api_token", None)
    response = client.get("/api/donations", headers={"X-Admin-Token": "anything"})
    assert response.status_code == 503


def test_invalid_volunteer_payload_is_rejected(client):
    response = client.post("/api/volunteers", json={"full_name": "x", "phone": "1"})
    assert response.status_code == 422
