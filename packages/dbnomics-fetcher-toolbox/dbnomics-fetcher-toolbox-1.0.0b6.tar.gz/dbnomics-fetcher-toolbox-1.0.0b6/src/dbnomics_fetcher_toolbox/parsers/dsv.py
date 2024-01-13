import csv

from dbnomics_fetcher_toolbox.parsers import FileParser
from dbnomics_fetcher_toolbox.parsers.errors import InvalidDsvDelimiter

__all__ = ["CsvFileParser", "DsvFileParser"]


class DsvFileParser(FileParser[str]):
    def __init__(self, *, allowed_delimiters: list[str], encoding: str | None = None) -> None:
        if allowed_delimiters is None:
            allowed_delimiters = ","
        self.allowed_delimiters = allowed_delimiters

        if encoding is None:
            encoding = "utf-8"
        self.encoding = encoding

    def _parse_bytes(self, content: bytes) -> str:
        resource_text = content.decode(self.encoding)
        validate_dsv_format(resource_text, allowed_delimiters=self.allowed_delimiters)
        return resource_text


class CsvFileParser(DsvFileParser):
    def __init__(self, *, encoding: str | None = None) -> None:
        super().__init__(allowed_delimiters=[","], encoding=encoding)


def validate_dsv_format(text: str, *, allowed_delimiters: list[str] | None) -> None:
    sniffer = csv.Sniffer()
    dialect = sniffer.sniff(text, delimiters=None if allowed_delimiters is None else "".join(allowed_delimiters))
    if allowed_delimiters is not None and dialect.delimiter not in allowed_delimiters:
        raise InvalidDsvDelimiter(allowed_delimiters=allowed_delimiters, detected_delimiter=dialect.delimiter)
