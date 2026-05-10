import pytest
from fastapi.testclient import TestClient
from wordpress_analyser.api import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "version" in body


def test_analyse_plugin(plugin_file):
    with open(plugin_file, "rb") as f:
        response = client.post(
            "/analyse",
            files={"file": ("my-plugin.php", f, "application/octet-stream")},
        )
    assert response.status_code == 200
    data = response.json()
    assert data["action_count"] == 2
    assert data["filter_count"] == 2
    assert data["detected_type"] == "plugin"


def test_analyse_non_php():
    response = client.post(
        "/analyse",
        files={"file": ("notes.txt", b"some content", "text/plain")},
    )
    assert response.status_code == 400
    assert ".php" in response.json()["detail"]
