"""Capability manifest for the lens family (consumed by auto-analyser)."""
from __future__ import annotations

from lens_contract import make_manifest

MANIFEST = make_manifest(
    name="wordpress-analyser",
    accepts=["wordpress", "php"],
    extensions=[".php"],
    auto_routable=True,
    produces="WordPressAnalysisResult",
)
