"""Smoke tests for the packaged CLI."""

import subprocess
import sys
from importlib.metadata import version
from pathlib import Path

from saltline.cli import main


def test_main_returns_success() -> None:
    assert main([]) == 0


def test_console_script_help() -> None:
    result = subprocess.run(
        [str(Path(sys.executable).with_name("saltline")), "--help"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "usage: saltline" in result.stdout


def test_console_script_version() -> None:
    result = subprocess.run(
        [str(Path(sys.executable).with_name("saltline")), "--version"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert result.stdout.strip() == f"saltline {version('saltline')}"
