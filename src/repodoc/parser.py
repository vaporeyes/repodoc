"""Parser for repomix output."""

import subprocess
from enum import Enum
from pathlib import Path
from typing import Optional

from repodoc.errors import InputFileError


class OutputFormat(Enum):
    """Output format for repomix."""

    MARKDOWN = "markdown"
    XML = "xml"
    TEXT = "text"


def run_repomix(
    repo_path: Path,
    format: OutputFormat = OutputFormat.MARKDOWN,
    compress: bool = False,
) -> Path:
    """Run repomix binary on a repository.

    Args:
        repo_path: Path to the Git repository.
        format: Output format for repomix (markdown, xml, or text).
        compress: Whether to compress the output.

    Returns:
        Path to the generated output file.

    Raises:
        InputFileError: If repomix fails or repository is invalid.
    """
    if not repo_path.exists():
        raise InputFileError(f"Repository not found: {repo_path}")

    if not (repo_path / ".git").exists():
        raise InputFileError(f"Not a Git repository: {repo_path}")

    extension = {
        OutputFormat.MARKDOWN: ".md",
        OutputFormat.XML: ".xml",
        OutputFormat.TEXT: ".txt",
    }[format]
    output_path = repo_path / f"repomix-output{extension}"

    cmd = [
        "npx",
        "--yes",
        "repomix",
        str(repo_path),
        "-o",
        str(output_path),
        "--style",
        format.value,
    ]
    if compress:
        cmd.append("--compress")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        raise InputFileError(f"repomix failed: {e.stderr}") from e
    except FileNotFoundError:
        raise InputFileError("repomix binary not found. Please install it first.")

    if not output_path.exists():
        raise InputFileError("repomix did not generate output file")

    return output_path