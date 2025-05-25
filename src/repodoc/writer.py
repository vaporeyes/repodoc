"""Safe markdown file writer."""

import os
import tempfile
from pathlib import Path
from typing import Dict

from repodoc.errors import OutputDirectoryError


# Mapping of documentation kinds to filenames
KIND_TO_FILENAME: Dict[str, str] = {
    "api": "api-docs.md",
    "manual": "user-manual.md",
    "architecture": "architecture.md",
}


def write(doc: str, kind: str, out_dir: Path) -> Path:
    """Write documentation to a markdown file.

    Args:
        doc: Documentation content to write.
        kind: Type of documentation (api, manual, architecture).
        out_dir: Directory to write the file to.

    Returns:
        Path to the written file.

    Raises:
        OutputDirectoryError: If the output directory cannot be created or is not writable.
        KeyError: If the documentation kind is not recognized.
    """
    # Ensure output directory exists
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        raise OutputDirectoryError(f"Failed to create output directory: {e}")

    # Get filename for the documentation kind
    try:
        filename = KIND_TO_FILENAME[kind]
    except KeyError:
        raise KeyError(f"Unknown documentation kind: {kind}")

    # Full path to the output file
    out_file = out_dir / filename

    # Write to a temporary file first
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=out_dir,
            delete=False
        ) as tmp:
            tmp.write(doc)
            tmp.write("\n")  # Ensure file ends with newline
            tmp_path = Path(tmp.name)

        # Atomically rename the temporary file to the target file
        os.replace(tmp_path, out_file)
    except OSError as e:
        # Clean up temporary file if it exists
        if tmp_path.exists():
            tmp_path.unlink()
        raise OutputDirectoryError(f"Failed to write documentation: {e}")

    return out_file 