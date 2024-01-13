from collections.abc import Iterator
from typing import TypeVar

import msgspec

from dbnomics_fetcher_toolbox.serializers.base import Serializer

__all__ = ["MsgspecJsonSerializer"]


T = TypeVar("T")


class MsgspecJsonSerializer(Serializer[T]):
    def __init__(self, *, encoding: str | None = None, pretty_print: bool = True) -> None:
        if encoding is None:
            encoding = "utf-8"
        self.encoding = encoding

        self.pretty_print = pretty_print

    def serialize(self, value: T) -> Iterator[bytes]:
        value_bytes = msgspec.json.encode(value)
        if self.pretty_print:
            yield msgspec.json.format(value_bytes)
        else:
            yield value_bytes
