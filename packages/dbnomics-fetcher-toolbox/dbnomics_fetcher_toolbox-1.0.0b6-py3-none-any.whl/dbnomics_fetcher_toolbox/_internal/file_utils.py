from collections.abc import Iterator
from pathlib import Path

import daiquiri
from dbnomics_data_model.file_utils import write_gitignore_all
from humanfriendly import format_size

logger = daiquiri.getLogger(__name__)


def create_directory(directory: Path, *, kind: str, with_gitignore: bool = False) -> None:
    if directory.is_dir():
        logger.debug("Using the existing directory %r as the %s directory", str(directory), kind)
        return
    try:
        directory.mkdir(exist_ok=True, parents=True)
    except OSError as exc:
        from dbnomics_fetcher_toolbox.errors.downloader import DirectoryCreateError

        raise DirectoryCreateError(directory, kind=kind) from exc

    if with_gitignore:
        write_gitignore_all(directory, exist_ok=True)

    logger.debug("Created %s directory: %r", kind, str(directory))


def format_file_path_with_size(file_path: Path) -> str:
    path_str = f"{str(file_path)!r}"
    size_str = format_size(file_path.stat().st_size, binary=True) if file_path.exists() else "does not exist"
    return f"{path_str} ({size_str})"


def is_directory_empty(directory: Path) -> bool:
    return not any(directory.iterdir())


def move_file(src: Path, dest: Path) -> None:
    dest.parent.mkdir(exist_ok=True, parents=True)
    src.rename(dest)


def write_chunks(
    chunks: Iterator[bytes],
    *,
    output_file: Path,
    page_size: int = 1024,
    message_interval: int = 1024,
) -> None:
    total_bytes_written = 0
    page_num = 1

    partial_output_file = output_file.with_suffix(f"{output_file.suffix}.part")

    # Avoid creating an empty file if the first chunk fails loading.
    try:
        chunk = next(chunks)
    except StopIteration:
        return

    with partial_output_file.open("wb") as fp:
        while True:
            fp.write(chunk)
            total_bytes_written += len(chunk)

            if total_bytes_written >= page_size * page_num * message_interval:
                logger.debug("%s bytes have been written so far", format_size(total_bytes_written, binary=True))
                page_num += 1

            try:
                chunk = next(chunks)
            except StopIteration:
                break

    partial_output_file.replace(output_file)
