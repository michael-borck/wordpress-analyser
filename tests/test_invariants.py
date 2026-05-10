"""Invariant tests — fast, run by default."""

from importlib.metadata import version

import pytest


def test_package_imports_cleanly() -> None:
    """Smoke alarm — package must import without errors."""
    import wordpress_analyser  # noqa: F401
    from wordpress_analyser.cli import main  # noqa: F401
    from wordpress_analyser.api import app  # noqa: F401


def test_health_version_matches_installed_package() -> None:
    """/health must report the actual installed package version."""
    from fastapi.testclient import TestClient

    from wordpress_analyser.api import app

    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["version"] == version("wordpress-analyser")


def test_app_version_matches_installed_package() -> None:
    """FastAPI app.version must match installed package."""
    from wordpress_analyser.api import app

    assert app.version == version("wordpress-analyser")


def test_non_php_input_handled_gracefully(tmp_path) -> None:
    """Analysing a non-PHP file returns a loud error, not a crash.

    Family pattern: failures are loud (error field set), not silent zero-fill.
    """
    from wordpress_analyser.core import analyse_file

    txt = tmp_path / "notes.txt"
    txt.write_text("This is not PHP.")
    result = analyse_file(txt)
    assert result.error is not None
    assert "php" in result.error.lower()
