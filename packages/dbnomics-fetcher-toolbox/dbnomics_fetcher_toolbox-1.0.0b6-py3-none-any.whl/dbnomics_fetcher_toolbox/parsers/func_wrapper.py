from pathlib import Path
from typing import TypeVar

from dbnomics_fetcher_toolbox.parsers import FileParser
from dbnomics_fetcher_toolbox.parsers.base import FileParserCallable

__all__ = ["FuncWrapperFileParser"]


T = TypeVar("T")


class FuncWrapperFileParser(FileParser[T]):
    def __init__(self, func: FileParserCallable[T]) -> None:
        self.func = func

    def _parse_file(self, input_file: Path) -> T:
        return self.func(input_file)
