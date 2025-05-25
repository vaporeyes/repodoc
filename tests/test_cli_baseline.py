"""Baseline tests for the CLI."""

from typer.testing import CliRunner

from repodoc.cli import app

runner = CliRunner()


def test_version() -> None:
    """Test --version option."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert result.stdout.strip() == "0.0.1"


def test_generate() -> None:
    """Test generate command."""
    result = runner.invoke(app, ["generate"])
    assert result.exit_code == 1
    assert result.stdout.strip() == "TODO" 