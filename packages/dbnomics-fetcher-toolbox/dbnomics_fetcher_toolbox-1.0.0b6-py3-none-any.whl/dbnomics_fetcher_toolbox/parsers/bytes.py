from dbnomics_fetcher_toolbox.parsers.base import FileParser


class BytesFileParser(FileParser[bytes]):
    """A file parser that does nothing: it just returns the bytes of the file as-is."""

    def _parse_bytes(self, content: bytes) -> bytes:
        return content
