from pathlib import Path
from zipfile import ZipFile

from dbnomics_fetcher_toolbox.sources.errors.base import SourceError
from dbnomics_fetcher_toolbox.sources.zip_utils import format_zip_filename


class ZipFileExtractError(SourceError):
    def __init__(self, *, file_to_extract: Path, zip_file: ZipFile) -> None:
        msg = f"Error extracting file {str(file_to_extract)!r} from ZIP file {format_zip_filename(zip_file)}"
        super().__init__(msg=msg)
