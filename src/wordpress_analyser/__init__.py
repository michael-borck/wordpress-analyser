from importlib.metadata import version as _v
from pathlib import Path

from .core import analyse_file
from .manifest import MANIFEST
from .models import WordPressAnalysisResult

__version__ = _v("wordpress-analyser")
del _v

# Canonical result-model alias for a uniform family surface.
WordPressAnalysis = WordPressAnalysisResult


class WordPressAnalyser:
    """Thin facade over the module-level ``analyse_file`` function."""

    def analyse(self, path: str | Path) -> WordPressAnalysisResult:
        return analyse_file(Path(path))


def analyse(path: str | Path) -> WordPressAnalysisResult:
    """Analyse a WordPress PHP file and return signals."""
    return WordPressAnalyser().analyse(Path(path))


__all__ = [
    "WordPressAnalyser",
    "WordPressAnalysis",
    "WordPressAnalysisResult",
    "analyse",
    "MANIFEST",
    "__version__",
]
