import tempfile
from contextlib import contextmanager
from pathlib import Path

from os import chdir as _chdir
from os import getcwd
from typing import Generator


@contextmanager
def chdir(cd: str | bytes | Path) -> Generator[None, None, None]:
    old = getcwd()
    _chdir(cd)
    try:
        yield
    finally:
        _chdir(old)


def test_everything(tmp_path: Path):
    with chdir(tmp_path):
        pass
