import pytest
from fastapi.testclient import TestClient
from wordpress_analyser.api import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_analyse_plugin(plugin_file):
    with open(plugin_file, "rb") as f:
        response = client.post(
            "/analyse",
            files={"file": ("my-plugin.php", f, "application/octet-stream")},
        )
    assert response.status_code == 200
    data = response.json()
    assert "action_count" in data
    assert data["action_count"] >= 2


def test_analyse_non_php():
    response = client.post(
        "/analyse",
        files={"file": ("notes.txt", b"some content", "text/plain")},
    )
    assert response.status_code == 400
