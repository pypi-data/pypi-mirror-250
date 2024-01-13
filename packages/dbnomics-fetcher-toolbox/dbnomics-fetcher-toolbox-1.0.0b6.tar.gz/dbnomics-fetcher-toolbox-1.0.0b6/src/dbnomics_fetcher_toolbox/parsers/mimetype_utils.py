from pathlib import Path  # noqa: I001


import pylibmagic  # Import before "magic"  # type: ignore[import-not-found]  # noqa: F401
import magic

from dbnomics_fetcher_toolbox.parsers.errors import InvalidMimeType


def detect_mimetype(source: Path | bytes | str) -> str:
    """Detect the MIME type of a source."""
    if isinstance(source, Path):
        return magic.from_file(source, mime=True)
    if isinstance(source, bytes | str):
        return magic.from_buffer(source, mime=True)

    msg = f"Unexpected source type: {type(source).__name__!r}"
    raise TypeError(msg)


def validate_mimetype(source: Path | bytes | str, *, expected_mimetype: str) -> None:
    detected_mimetype = detect_mimetype(source)
    if detected_mimetype != expected_mimetype:
        raise InvalidMimeType(detected_mimetype=detected_mimetype, expected_mimetype=expected_mimetype)
