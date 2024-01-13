from collections.abc import Iterator
from pathlib import Path

__all__ = ["iter_child_directories"]


def iter_child_directories(base_dir: Path, *, ignore_hidden: bool = True) -> Iterator[Path]:
    """Iterate over child directories of base_dir."""
    for child in base_dir.iterdir():
        if not child.is_dir():
            continue

        dir_name = child.name
        if ignore_hidden and dir_name.startswith("."):
            continue

        yield child
