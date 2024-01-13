from abc import ABC, abstractmethod
from collections.abc import Iterator
from pathlib import Path
from typing import TYPE_CHECKING, TypeVar

import daiquiri

if TYPE_CHECKING:
    from dbnomics_fetcher_toolbox.types import ResourceFullId


__all__ = ["Source"]

logger = daiquiri.getLogger(__name__)


T = TypeVar("T")


class Source(ABC):
    @abstractmethod
    def iter_bytes(self, *, debug_dir: Path | None, resource_full_id: "ResourceFullId") -> Iterator[bytes]:
        ...
