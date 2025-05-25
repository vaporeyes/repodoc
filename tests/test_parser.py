"""Tests for the repomix execution."""

import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest

from repodoc.errors import InputFileError
from repodoc.parser import OutputFormat, run_repomix


@pytest.fixture
def mock_repo(tmp_path: Path) -> Path:
    """Create a mock Git repository.

    Args:
        tmp_path: Pytest fixture providing temporary directory.

    Returns:
        Path to the mock repository.
    """
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / ".git").mkdir()
    return repo


def test_run_repomix_success_markdown(mock_repo: Path) -> None:
    """Test successful repomix execution with markdown format.

    Args:
        mock_repo: Path to mock repository.
    """
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = subprocess.CompletedProcess(
            ["repomix"], 0, stdout="", stderr=""
        )
        with patch("pathlib.Path.exists", return_value=True):
            output_path = run_repomix(mock_repo, format=OutputFormat.MARKDOWN)
            assert output_path == mock_repo / "repomix-output.md"
            mock_run.assert_called_once_with(
                [
                    "npx",
                    "--yes",
                    "repomix",
                    str(mock_repo),
                    "-o",
                    str(output_path),
                    "--style",
                    "markdown",
                ],
                capture_output=True,
                text=True,
                check=True,
            )


def test_run_repomix_success_xml(mock_repo: Path) -> None:
    """Test successful repomix execution with XML format.

    Args:
        mock_repo: Path to mock repository.
    """
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = subprocess.CompletedProcess(
            ["repomix"], 0, stdout="", stderr=""
        )
        with patch("pathlib.Path.exists", return_value=True):
            output_path = run_repomix(mock_repo, format=OutputFormat.XML)
            assert output_path == mock_repo / "repomix-output.xml"
            mock_run.assert_called_once_with(
                [
                    "npx",
                    "--yes",
                    "repomix",
                    str(mock_repo),
                    "-o",
                    str(output_path),
                    "--style",
                    "xml",
                ],
                capture_output=True,
                text=True,
                check=True,
            )


def test_run_repomix_success_text(mock_repo: Path) -> None:
    """Test successful repomix execution with text format.

    Args:
        mock_repo: Path to mock repository.
    """
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = subprocess.CompletedProcess(
            ["repomix"], 0, stdout="", stderr=""
        )
        with patch("pathlib.Path.exists", return_value=True):
            output_path = run_repomix(mock_repo, format=OutputFormat.TEXT)
            assert output_path == mock_repo / "repomix-output.txt"
            mock_run.assert_called_once_with(
                [
                    "npx",
                    "--yes",
                    "repomix",
                    str(mock_repo),
                    "-o",
                    str(output_path),
                    "--style",
                    "text",
                ],
                capture_output=True,
                text=True,
                check=True,
            )


def test_run_repomix_with_compression(mock_repo: Path) -> None:
    """Test successful repomix execution with compression enabled.

    Args:
        mock_repo: Path to mock repository.
    """
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = subprocess.CompletedProcess(
            ["repomix"], 0, stdout="", stderr=""
        )
        with patch("pathlib.Path.exists", return_value=True):
            output_path = run_repomix(mock_repo, compress=True)
            assert output_path == mock_repo / "repomix-output.md"
            mock_run.assert_called_once_with(
                [
                    "npx",
                    "--yes",
                    "repomix",
                    str(mock_repo),
                    "-o",
                    str(output_path),
                    "--style",
                    "markdown",
                    "--compress",
                ],
                capture_output=True,
                text=True,
                check=True,
            )


def test_run_repomix_not_git(mock_repo: Path) -> None:
    """Test running repomix on non-Git directory.

    Args:
        mock_repo: Path to mock repository.
    """
    (mock_repo / ".git").rmdir()
    with pytest.raises(InputFileError, match="Not a Git repository"):
        run_repomix(mock_repo)


def test_run_repomix_not_found(mock_repo: Path) -> None:
    """Test running repomix when binary not found.

    Args:
        mock_repo: Path to mock repository.
    """
    with patch("subprocess.run", side_effect=FileNotFoundError):
        with pytest.raises(InputFileError, match="repomix binary not found"):
            run_repomix(mock_repo)


def test_run_repomix_failure(mock_repo: Path) -> None:
    """Test repomix execution failure.

    Args:
        mock_repo: Path to mock repository.
    """
    with patch(
        "subprocess.run",
        side_effect=subprocess.CalledProcessError(1, "repomix", stderr="Error"),
    ):
        with pytest.raises(InputFileError, match="repomix failed"):
            run_repomix(mock_repo)
