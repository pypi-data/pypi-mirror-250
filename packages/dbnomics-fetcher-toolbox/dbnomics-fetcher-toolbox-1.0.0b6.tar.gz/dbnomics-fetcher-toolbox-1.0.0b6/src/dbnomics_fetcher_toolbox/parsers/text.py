from dbnomics_fetcher_toolbox.parsers import FileParser
from dbnomics_fetcher_toolbox.parsers.mimetype_utils import validate_mimetype

__all__ = ["TextFileParser"]


class TextFileParser(FileParser[str]):
    def __init__(self, *, encoding: str | None = None, mime_type: str | None = None) -> None:
        if encoding is None:
            encoding = "utf-8"
        self.encoding = encoding

        self.mime_type = mime_type

    def _parse_bytes(self, content: bytes) -> str:
        if self.mime_type is not None:
            validate_mimetype(content, expected_mimetype=self.mime_type)
        return content.decode(self.encoding)
