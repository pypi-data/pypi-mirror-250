from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING
from zipfile import ZipFile

import daiquiri
from contexttimer import Timer
from humanfriendly import format_size

from dbnomics_fetcher_toolbox._internal.formatting_utils import format_timer
from dbnomics_fetcher_toolbox.sources.base import Source
from dbnomics_fetcher_toolbox.sources.errors.zip import ZipFileExtractError
from dbnomics_fetcher_toolbox.sources.zip_utils import format_zip_filename

if TYPE_CHECKING:
    from dbnomics_fetcher_toolbox.types import ResourceFullId

__all__ = ["ZipFileExtractor"]


logger = daiquiri.getLogger(__name__)


@dataclass(frozen=True, init=False)
class ZipFileExtractor(Source):
    file_to_extract: Path
    zip_file: ZipFile

    def __init__(self, *, file_to_extract: str | Path, zip_file: ZipFile) -> None:
        if isinstance(file_to_extract, str):
            file_to_extract = Path(file_to_extract)
        if file_to_extract.is_absolute():
            msg = (
                f"file_to_extract must be relative to the ZIP file, but got an absolute path: {str(file_to_extract)!r}"
            )
            raise RuntimeError(msg)
        object.__setattr__(self, "file_to_extract", file_to_extract)

        object.__setattr__(self, "zip_file", zip_file)

    def iter_bytes(
        self, *, debug_dir: Path | None, resource_full_id: "ResourceFullId"  # noqa: ARG002
    ) -> Iterator[bytes]:
        file_to_extract = self.file_to_extract
        zip_file = self.zip_file

        logger.debug(
            "Extracting bytes of file %r from ZIP file %s",
            str(file_to_extract),
            format_zip_filename(zip_file),
            resource_full_id=resource_full_id,
        )

        try:
            with Timer() as timer:
                file_to_extract_bytes = zip_file.read(str(file_to_extract))
        except KeyError as exc:
            raise ZipFileExtractError(file_to_extract=file_to_extract, zip_file=zip_file) from exc

        logger.debug(
            "Extracted bytes of file %r (%s) from ZIP file %s successfully",
            str(file_to_extract),
            format_size(len(file_to_extract_bytes)),
            format_zip_filename(zip_file),
            duration=format_timer(timer),
            resource_full_id=resource_full_id,
        )
        yield file_to_extract_bytes
