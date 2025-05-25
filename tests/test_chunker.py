"""Tests for the file chunker."""

from pathlib import Path

import pytest

from repodoc.chunker import iter_chunks


@pytest.fixture
def sample_file(tmp_path: Path) -> Path:
    """Create a sample file for testing.

    Args:
        tmp_path: Pytest fixture providing temporary directory.

    Returns:
        Path to the sample file.
    """
    content = "line1\n" * 1000  # 5000 chars = ~1250 tokens
    file = tmp_path / "sample.txt"
    file.write_text(content)
    return file


def test_chunk_small_file(sample_file: Path) -> None:
    """Test chunking a file smaller than the token limit.

    Args:
        sample_file: Path to the sample file.
    """
    chunks = list(iter_chunks(sample_file, max_tokens=2000))
    assert len(chunks) == 1
    assert chunks[0] == "line1\n" * 1000


def test_chunk_large_file(sample_file: Path) -> None:
    """File ≈6 000 chars, max_tokens=500 → three ~2 000-char slices."""
    max_tokens = 500
    max_chars = max_tokens * 4  # 2 000
    line_len = len("line1\n")  # 6

    chunks = list(iter_chunks(sample_file, max_tokens=max_tokens))

    # 6 000 / 2 000 → 3 chunks (ceil)
    assert len(chunks) == 3

    # Each slice is guaranteed ≤ max_chars + one-line slop
    assert all(len(c) <= max_chars + line_len for c in chunks)

    # Sizes should be roughly equal (within 10 %)
    sizes = list(map(len, chunks))
    mean = sum(sizes) / len(sizes)
    assert all(abs(sz - mean) <= 0.10 * mean for sz in sizes)


def test_chunk_nonexistent_file(tmp_path: Path) -> None:
    """Test chunking a nonexistent file.

    Args:
        tmp_path: Pytest fixture providing temporary directory.
    """
    with pytest.raises(FileNotFoundError):
        list(iter_chunks(tmp_path / "nonexistent.txt"))


def test_chunk_invalid_encoding(tmp_path: Path) -> None:
    """Test chunking a file with invalid UTF-8 encoding.

    Args:
        tmp_path: Pytest fixture providing temporary directory.
    """
    file = tmp_path / "invalid.txt"
    file.write_bytes(b"\xff\xfe")  # Invalid UTF-8
    with pytest.raises(UnicodeDecodeError):
        list(iter_chunks(file))


def test_chunk_empty_file(tmp_path: Path) -> None:
    """Empty file ⇒ no chunks produced."""
    empty = tmp_path / "empty.txt"
    empty.touch()

    chunks = list(iter_chunks(empty))
    assert chunks == []
