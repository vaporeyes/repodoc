"""File chunking functionality for large text files."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Iterator


def iter_chunks(path: Path, *, max_tokens: int = 16_000) -> Iterator[str]:
    """Yield slices of *text* that stay within the token limit and are
    approximately equal in size.

    A conservative 4 chars ≈ 1 token heuristic is used. Since we're trying to
    send this to Ollama, we need to make sure the chunks are not too large. (for now)
    """
    max_chars = max_tokens * 4

    # ---- quick file-size estimate (bytes ≈ chars for UTF-8 ASCII-heavy code)
    total_bytes = path.stat().st_size
    total_chars_est = max(total_bytes, 1)  # avoid div/0

    # minimum chunks so each is ≤ max_chars
    num_chunks = math.ceil(total_chars_est / max_chars)
    target_chars = math.ceil(total_chars_est / num_chunks)

    # (defensive) guarantee target ≤ hard limit
    target_chars = min(target_chars, max_chars)

    buf: list[str] = []
    char_count = 0

    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            buf.append(line)
            char_count += len(line)

            # If we’ve crossed the *target* and emitting would still honour
            # the hard cap, flush the buffer.
            if char_count >= target_chars:
                yield "".join(buf)
                buf.clear()
                char_count = 0

    if buf:  # trailing remainder
        yield "".join(buf)
