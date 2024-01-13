from collections.abc import Callable
from typing import TYPE_CHECKING, TypeAlias

if TYPE_CHECKING:
    from dbnomics_fetcher_toolbox.bisect.partitions.dimension.___model import BisectDimension


BisectDimensionCode: TypeAlias = str
BisectDimensionValueCode: TypeAlias = str
SeriesMask: TypeAlias = str


DimensionSelector: TypeAlias = Callable[[list["BisectDimension"]], BisectDimensionCode]
PartitionIdBuilder: TypeAlias = Callable[[list["BisectDimension"]], PartitionId]
