import os
from pathlib import Path
from contextlib import contextmanager

@contextmanager
def as_cwd(path: Path):
    prev = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev)