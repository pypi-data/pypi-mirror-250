from typing import TypeVar, cast

import msgspec
from jsonalias import Json

from dbnomics_fetcher_toolbox.parsers import FileParser
from dbnomics_fetcher_toolbox.serializers.base import Serializer
from dbnomics_fetcher_toolbox.serializers.json.msgspec import MsgspecJsonSerializer

__all__ = ["MsgspecJsonFileParser", "MsgspecTypedJsonFileParser"]


T = TypeVar("T")


class MsgspecJsonFileParser(FileParser[Json]):
    @property
    def default_serializer(self) -> Serializer[Json]:
        return MsgspecJsonSerializer()

    def _parse_bytes(self, content: bytes) -> Json:
        return cast(Json, msgspec.json.decode(content))


class MsgspecTypedJsonFileParser(FileParser[T]):
    def __init__(self, *, type: type[T]) -> None:
        self._type = type

    @property
    def default_serializer(self) -> Serializer[T]:
        return MsgspecJsonSerializer()

    def _parse_bytes(self, content: bytes) -> T:
        return msgspec.json.decode(content, type=self._type)
