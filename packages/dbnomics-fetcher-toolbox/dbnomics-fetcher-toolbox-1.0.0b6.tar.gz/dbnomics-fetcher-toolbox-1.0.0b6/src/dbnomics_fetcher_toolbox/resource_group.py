from abc import ABC, abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING, Any, Literal, TypeVar, overload

import daiquiri

from dbnomics_fetcher_toolbox.bisect.partitions.types import BisectionPartition
from dbnomics_fetcher_toolbox.resource import Resource
from dbnomics_fetcher_toolbox.types import ResourceGroupId

if TYPE_CHECKING:
    from dbnomics_fetcher_toolbox.downloader import Downloader
    from dbnomics_fetcher_toolbox.serializers.base import Serializer
    from dbnomics_fetcher_toolbox.sources.base import Source

__all__ = ["ResourceGroup"]


logger = daiquiri.getLogger(__name__)


T = TypeVar("T")
TBisectionPartition = TypeVar("TBisectionPartition", bound=BisectionPartition)


class ResourceGroup(ABC):
    def __init__(self, *, id: str) -> None:
        id = ResourceGroupId.parse(id)
        self.id = id

    def __repr__(self) -> str:
        return f"{type(self).__name__}(id={self.id!r})"

    @overload
    def process_resource(
        self,
        resource: Resource[T],
        *,
        keep: bool = True,
        required: Literal[True] = True,
        serializer: "Serializer[T] | None" = None,
        source: "Source",
        updated_at: datetime | None = None,
    ) -> T:
        ...

    @overload
    def process_resource(
        self,
        resource: Resource[T],
        *,
        keep: bool = True,
        required: Literal[False],
        serializer: "Serializer[T] | None" = None,
        source: "Source",
        updated_at: datetime | None = None,
    ) -> T | None:
        ...

    @overload
    def process_resource(
        self,
        resource: Resource[T],
        *,
        keep: bool = True,
        required: bool = True,
        serializer: "Serializer[T] | None" = None,
        source: "Source",
        updated_at: datetime | None = None,
    ) -> T | None:
        ...

    def process_resource(
        self,
        resource: Resource[T],
        *,
        keep: bool = True,
        required: bool = True,
        serializer: "Serializer[T] | None" = None,
        source: "Source",
        updated_at: datetime | None = None,
    ) -> T | None:
        return self._downloader._process_group_resource(  # noqa: SLF001
            resource,
            group=self,
            keep=keep,
            required=required,
            serializer=serializer,
            source=source,
            updated_at=updated_at,
        )

    @abstractmethod
    def _process(self) -> None:
        ...

    def _start(self, *, downloader: "Downloader") -> None:
        self._downloader = downloader
        self._kept_resources: list[Resource[Any]] = []
        self._process()
