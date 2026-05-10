import json
import subprocess
import sys
from pathlib import Path

from conftest import PLUGIN_PHP

# Resolve the venv python for the project so subprocess calls find wordpress_analyser
_PROJECT_ROOT = Path(__file__).parent.parent
_VENV_PYTHON = _PROJECT_ROOT / ".venv" / "bin" / "python"

# Fall back to sys.executable when running inside the venv already
_PYTHON = str(_VENV_PYTHON) if _VENV_PYTHON.exists() else sys.executable


def test_help_exits_zero():
    result = subprocess.run(
        [_PYTHON, "-m", "wordpress_analyser.cli", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "wordpress-analyser" in result.stdout


def test_serve_help_exits_zero():
    result = subprocess.run(
        [_PYTHON, "-m", "wordpress_analyser.cli", "serve", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "serve" in result.stdout


def test_cli_analyse_plugin_file(tmp_path):
    """CLI analysing a plugin file prints expected content."""
    plugin = tmp_path / "test-plugin.php"
    plugin.write_text(PLUGIN_PHP)

    proc = subprocess.run(
        [_PYTHON, "-m", "wordpress_analyser.cli", str(plugin)],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    # Default output is rich/text; check for substring of meaningful output
    assert "plugin" in proc.stdout.lower()


def test_cli_json_output(tmp_path):
    """--json flag emits parseable JSON with expected fields."""
    plugin = tmp_path / "test-plugin.php"
    plugin.write_text(PLUGIN_PHP)

    proc = subprocess.run(
        [_PYTHON, "-m", "wordpress_analyser.cli", str(plugin), "--json"],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    data = json.loads(proc.stdout)
    assert "action_count" in data
    assert data["action_count"] >= 1
    assert "detected_type" in data


def test_cli_nonexistent_file_exits_nonzero(tmp_path):
    """Missing file: non-zero exit, no crash."""
    proc = subprocess.run(
        [_PYTHON, "-m", "wordpress_analyser.cli", str(tmp_path / "missing.php")],
        capture_output=True,
        text=True,
    )
    assert proc.returncode != 0
