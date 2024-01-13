from typing import TYPE_CHECKING

from dbnomics_fetcher_toolbox.errors.base import FetcherToolboxError

if TYPE_CHECKING:
    from dbnomics_fetcher_toolbox.bisect.partitions.types import BisectionPartition


class BisectionError(FetcherToolboxError):
    pass


class PartitionBisectionError(BisectionError):
    def __init__(self, *, msg: str, partition: "BisectionPartition") -> None:
        super().__init__(msg=msg)
        self.partition = partition


class NoMoreBisectionError(PartitionBisectionError):
    def __init__(self, *, partition: "BisectionPartition") -> None:
        msg = f"Partition {partition.id!r} can't be bisected anymore"
        super().__init__(msg=msg, partition=partition)
