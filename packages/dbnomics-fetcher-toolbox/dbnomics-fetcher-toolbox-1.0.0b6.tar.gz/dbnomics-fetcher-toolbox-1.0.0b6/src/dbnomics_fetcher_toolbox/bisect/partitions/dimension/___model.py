from dataclasses import dataclass
from typing import TYPE_CHECKING

from dbnomics_fetcher_toolbox.bisect.errors import BisectDimensionNotFound

if TYPE_CHECKING:
    from dbnomics_fetcher_toolbox.bisect.partitions.dimension.__types import (
        BisectDimensionCode,
        BisectDimensionValueCode,
    )

__all__ = ["BisectDimension", "BisectDimensionValue"]


@dataclass(frozen=True, kw_only=True)
class BisectDimensionValue:
    code: "BisectDimensionValueCode"


@dataclass(frozen=True, kw_only=True)
class BisectDimension:
    code: "BisectDimensionCode"
    selected_values: list[BisectDimensionValue]
    total_num_values: int


def find_dimension_by_code(code: "BisectDimensionCode", dimensions: list[BisectDimension]) -> BisectDimension:
    for dimension in dimensions:
        if dimension.code == code:
            return dimension
    raise BisectDimensionNotFound(code, dimensions=dimensions)
