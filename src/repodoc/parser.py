"""Parser for repomix output."""

import subprocess
from pathlib import Path

from repodoc.errors import InputFileError


def run_repomix(repo_path: Path) -> Path:
    """Run repomix binary on a repository.

    Args:
        repo_path: Path to the Git repository.

    Returns:
        Path to the generated output file.

    Raises:
        InputFileError: If repomix fails or repository is invalid.
    """
    if not repo_path.exists():
        raise InputFileError(f"Repository not found: {repo_path}")

    if not (repo_path / ".git").exists():
        raise InputFileError(f"Not a Git repository: {repo_path}")

    output_path = repo_path / "repomix-output.txt"
    try:
        result = subprocess.run(
            ["repomix", str(repo_path), "-o", str(output_path)],
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
