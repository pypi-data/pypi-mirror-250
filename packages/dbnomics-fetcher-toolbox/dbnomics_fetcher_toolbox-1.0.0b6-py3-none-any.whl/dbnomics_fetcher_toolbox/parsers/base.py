from collections.abc import Callable
from pathlib import Path
from typing import TYPE_CHECKING, Generic, TypeAlias, TypeVar

import daiquiri
from contexttimer import Timer

from dbnomics_fetcher_toolbox._internal.file_utils import format_file_path_with_size
from dbnomics_fetcher_toolbox._internal.formatting_utils import format_timer

if TYPE_CHECKING:
    from dbnomics_fetcher_toolbox.serializers.base import Serializer


__all__ = ["FileParser"]


logger = daiquiri.getLogger(__name__)

T = TypeVar("T")

FileParserCallable: TypeAlias = Callable[[Path], T]


class FileParser(Generic[T]):
    @property
    def default_serializer(self) -> "Serializer[T] | None":
        return None

    def parse_file(self, input_file: Path) -> T:
        class_name = self.__class__.__name__
        with Timer() as timer:
            result = self._parse_file(input_file)
        logger.debug(
            "Parsed %s successfully with %s",
            format_file_path_with_size(input_file),
            class_name,
            duration=format_timer(timer),
        )
        return result

    def _parse_bytes(self, content: bytes) -> T:
        raise NotImplementedError

    def _parse_file(self, input_file: Path) -> T:
        content = input_file.read_bytes()
        return self._parse_bytes(content)
