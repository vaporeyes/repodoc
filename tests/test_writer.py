"""Tests for markdown writer."""

import os
import pytest
from pathlib import Path

from repodoc.errors import OutputDirectoryError
from repodoc.writer import write, KIND_TO_FILENAME


def test_write_new_file(tmp_path: Path) -> None:
    """Test writing to a new file.

    Args:
        tmp_path: Temporary directory provided by pytest.
    """
    doc = "Test documentation"
    out_file = write(doc, "api", tmp_path)
    
    assert out_file.exists()
    assert out_file.name == "api-docs.md"
    assert out_file.read_text() == "Test documentation\n"


def test_write_overwrite_file(tmp_path: Path) -> None:
    """Test overwriting an existing file.

    Args:
        tmp_path: Temporary directory provided by pytest.
    """
    # Write initial content
    write("Initial content", "api", tmp_path)
    
    # Overwrite with new content
    doc = "Updated documentation"
    out_file = write(doc, "api", tmp_path)
    
    assert out_file.exists()
    assert out_file.read_text() == "Updated documentation\n"


def test_write_all_kinds(tmp_path: Path) -> None:
    """Test writing all documentation kinds.

    Args:
        tmp_path: Temporary directory provided by pytest.
    """
    for kind, filename in KIND_TO_FILENAME.items():
        doc = f"Test {kind} documentation"
        out_file = write(doc, kind, tmp_path)
        
        assert out_file.exists()
        assert out_file.name == filename
        assert out_file.read_text() == f"Test {kind} documentation\n"


def test_write_unknown_kind(tmp_path: Path) -> None:
    """Test writing with unknown documentation kind.

    Args:
        tmp_path: Temporary directory provided by pytest.
    """
    with pytest.raises(KeyError, match="Unknown documentation kind: unknown"):
        write("Test doc", "unknown", tmp_path)


def test_write_unwritable_directory(tmp_path: Path) -> None:
    """Test writing to an unwritable directory.

    Args:
        tmp_path: Temporary directory provided by pytest.
    """
    # Make directory unwritable
    os.chmod(tmp_path, 0o444)
    
    try:
        with pytest.raises(OutputDirectoryError, match="Failed to create output directory"):
            write("Test doc", "api", tmp_path / "subdir")
    finally:
        # Restore permissions
        os.chmod(tmp_path, 0o755)


def test_write_unicode_content(tmp_path: Path) -> None:
    """Test writing unicode content.

    Args:
        tmp_path: Temporary directory provided by pytest.
    """
    doc = "Test documentation with unicode: 你好"
    out_file = write(doc, "api", tmp_path)
    
    assert out_file.exists()
    assert out_file.read_text() == "Test documentation with unicode: 你好\n" 