from dbnomics_fetcher_toolbox.errors.base import FetcherToolboxError


class InvalidDsvDelimiter(FetcherToolboxError):
    def __init__(self, *, allowed_delimiters: list[str], detected_delimiter: str) -> None:
        msg = f"The detected delimiter {detected_delimiter!r} is different from any of the allowed ones: {allowed_delimiters!r}"  # noqa: E501
        super().__init__(msg=msg)
        self.allowed_delimiters = allowed_delimiters
        self.detected_delimiter = detected_delimiter


class InvalidMimeType(FetcherToolboxError):
    def __init__(self, *, detected_mimetype: str, expected_mimetype: str) -> None:
        msg = f"The detected MIME type {detected_mimetype!r} is different from the expected one: {expected_mimetype!r}"
        super().__init__(msg=msg)
        self.detected_mimetype = detected_mimetype
        self.expected_mimetype = expected_mimetype
