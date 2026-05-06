import subprocess
import sys


def test_help_exits_zero():
    result = subprocess.run(
        ["uv", "run", "wordpress-analyser", "--help"],
        capture_output=True,
        text=True,
        cwd="/Users/michael/Projects/lens/wordpress-analyser",
    )
    assert result.returncode == 0


def test_serve_help_exits_zero():
    result = subprocess.run(
        ["uv", "run", "wordpress-analyser", "serve", "--help"],
        capture_output=True,
        text=True,
        cwd="/Users/michael/Projects/lens/wordpress-analyser",
    )
    assert result.returncode == 0
