from dataclasses import dataclass
from pathlib import Path
from typing import Generic, TypeVar

from dbnomics_fetcher_toolbox.parsers import FileParser
from dbnomics_fetcher_toolbox.parsers.base import FileParserCallable
from dbnomics_fetcher_toolbox.parsers.func_wrapper import FuncWrapperFileParser
from dbnomics_fetcher_toolbox.types import ResourceId

__all__ = ["Resource"]


T = TypeVar("T")


@dataclass(frozen=True, init=False)
class Resource(Generic[T]):
    file: Path
    id: ResourceId
    parser: FileParser[T]

    def __init__(
        self, *, file: str | Path, id: str | None = None, parser: FileParser[T] | FileParserCallable[T]
    ) -> None:
        if isinstance(file, str):
            file = Path(file)
        if file.is_absolute():
            msg = f"Resource file path must be relative to the target directory, but got an absolute path: {str(file)!r}"  # noqa: E501
            raise ValueError(msg)
        object.__setattr__(self, "file", file)

        if callable(parser):
            parser = FuncWrapperFileParser(parser)
        object.__setattr__(self, "parser", parser)

        if id is None:
            id = ResourceId.from_file_path(file)
        elif isinstance(id, str):
            id = ResourceId.parse(id)
        object.__setattr__(self, "id", id)
