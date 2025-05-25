"""Tests for command-line interface."""

import asyncio
import logging
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import typer
from typer.testing import CliRunner

from repodoc.cli import app, _generate_docs
from repodoc.errors import OutputDirectoryError
from repodoc.ollama import OllamaClient


@pytest.fixture
def runner() -> CliRunner:
    """Create CLI runner fixture.

    Returns:
        CliRunner instance.
    """
    return CliRunner()


@pytest.fixture
def mock_console() -> MagicMock:
    """Create mock console fixture.

    Returns:
        Mock console instance.
    """
    return MagicMock()


@pytest.mark.asyncio
async def test_generate_docs_success(tmp_path: Path, mock_console: MagicMock) -> None:
    """Test successful documentation generation.

    Args:
        tmp_path: Temporary directory provided by pytest.
        mock_console: Mock console instance.
    """
    # Create mock repository
    repo_path = tmp_path / "repo"
    repo_path.mkdir()
    (repo_path / ".git").mkdir()

    # Mock repomix output
    project_file = tmp_path / "project.txt"
    project_file.write_text("Test project content")

    # Mock Ollama client
    mock_client = AsyncMock(spec=OllamaClient)
    mock_client.generate.return_value = "Test documentation"

    with patch("repodoc.cli.run_repomix", return_value=project_file), \
         patch("repodoc.cli.OllamaClient", return_value=mock_client), \
         patch("repodoc.cli.setup_logging", return_value=mock_console), \
         patch("repodoc.cli.write") as mock_write, \
         patch("repodoc.cli.Confirm.ask", return_value=True):
        
        await _generate_docs(repo_path, tmp_path / "docs", verbose=True)
        
        # Get logger and verify its effective level
        logger = logging.getLogger("repodoc")
        assert logger.getEffectiveLevel() == logging.WARNING
        
        # Verify client was called for each generator
        assert mock_client.generate.call_count == 3
        
        # Verify files were written
        assert mock_write.call_count == 3


@pytest.mark.asyncio
async def test_generate_docs_error(tmp_path: Path, mock_console: MagicMock) -> None:
    """Test error handling during documentation generation.

    Args:
        tmp_path: Temporary directory provided by pytest.
        mock_console: Mock console instance.
    """
    # Create mock repository
    repo_path = tmp_path / "repo"
    repo_path.mkdir()
    (repo_path / ".git").mkdir()

    # Mock repomix output
    project_file = tmp_path / "project.txt"
    project_file.write_text("Test project content")

    # Mock Ollama client to raise an error
    mock_client = AsyncMock(spec=OllamaClient)
    mock_client.generate.side_effect = Exception("Test error")

    with patch("repodoc.cli.run_repomix", return_value=project_file), \
         patch("repodoc.cli.OllamaClient", return_value=mock_client), \
         patch("repodoc.cli.setup_logging", return_value=mock_console), \
         patch("repodoc.cli.Confirm.ask", return_value=False):
        
        with pytest.raises(typer.Exit):  # Changed from SystemExit
            await _generate_docs(repo_path, tmp_path / "docs", verbose=True)


def test_cli_help(runner: CliRunner) -> None:
    """Test CLI help output.

    Args:
        runner: CLI runner fixture.
    """
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    help_text = "Generate documentation from Git repositories using Ollama"
    assert help_text.lower() in result.output.lower()


def test_cli_verbose(runner: CliRunner, tmp_path: Path) -> None:
    """Test CLI verbose flag.

    Args:
        runner: CLI runner fixture.
        tmp_path: Temporary directory provided by pytest.
    """
    # Create mock repository with .git directory
    repo_path = tmp_path / "repo"
    repo_path.mkdir()
    (repo_path / ".git").mkdir()

    print(type(repo_path))
    print(repo_path)
    print(repo_path.absolute())

    with patch("repodoc.cli._generate_docs") as mock_generate:
        # Use absolute path to avoid any path resolution issues
        result = runner.invoke(app, [str(repo_path.absolute()), "-v"])
        print(result.output)
        assert result.exit_code == 0
        mock_generate.assert_called_once()
        assert mock_generate.call_args[0][2] is True  # verbose=True 