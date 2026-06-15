import wordpress_analyser as wa
from wordpress_analyser import (
    MANIFEST,
    WordPressAnalyser,
    WordPressAnalysis,
    __version__,
    analyse,
)


def test_canonical_names_import():
    assert WordPressAnalyser is not None
    assert WordPressAnalysis is not None


def test_analyse_is_callable():
    assert callable(analyse)


def test_manifest_name():
    assert MANIFEST["name"] == "wordpress-analyser"


def test_version_is_str():
    assert isinstance(__version__, str)


def test_names_in_all():
    for name in [
        "WordPressAnalyser",
        "WordPressAnalysis",
        "analyse",
        "MANIFEST",
        "__version__",
    ]:
        assert name in wa.__all__
