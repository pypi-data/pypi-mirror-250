from collections.abc import Iterator
from pathlib import Path
from typing import Any

from dbnomics_fetcher_toolbox.serializers.json.msgspec import MsgspecJsonSerializer
from dbnomics_fetcher_toolbox.sources.base import Source
from dbnomics_fetcher_toolbox.types import ResourceFullId

__all__ = ["MsgspecJsonSource"]


class MsgspecJsonSource(Source):
    def __init__(self, data: Any, *, encoding: str | None = None, pretty_print: bool = True) -> None:
        self.data = data
        self.serializer: MsgspecJsonSerializer[Any] = MsgspecJsonSerializer(
            encoding=encoding, pretty_print=pretty_print
        )

    def iter_bytes(
        self, *, debug_dir: Path | None, resource_full_id: ResourceFullId  # noqa: ARG002
    ) -> Iterator[bytes]:
        yield from self.serializer.serialize(self.data)
