from pathlib import Path
from zipfile import ZipFile

from dbnomics_fetcher_toolbox.parsers import FileParser

__all__ = ["ZipFileParser"]


class ZipFileParser(FileParser[ZipFile]):
    def _parse_file(self, input_file: Path) -> ZipFile:
        return ZipFile(input_file)
