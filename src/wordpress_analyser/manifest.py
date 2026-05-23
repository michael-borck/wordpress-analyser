"""Capability manifest for the lens family (consumed by auto-analyser)."""
from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version


def _version() -> str:
    try:
        return version("wordpress-analyser")
    except PackageNotFoundError:
        return "0.0.0"


MANIFEST: dict = {
    "name": "wordpress-analyser",
    "version": _version(),
    "role": "analyser",
    "accepts": ["wordpress", "php"],
    "extensions": [".php"],
    "auto_routable": True,
    "produces": "WordPressAnalysisResult",
}
