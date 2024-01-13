from dataclasses import dataclass, field

from dbnomics_fetcher_toolbox.bisect.partitions.dimension.___model import BisectDimension
from dbnomics_fetcher_toolbox.bisect.partitions.dimension.__types import SeriesMask

__all__ = ["SeriesMaskBuilder"]


@dataclass(frozen=True, kw_only=True)
class SeriesMaskBuilder:
    all_values_selected_char: str = field(default="")
    dimension_delimiter: str = field(default=".")
    dimension_value_delimiter: str = field(default="+")

    def build_series_mask(self, dimensions: list[BisectDimension]) -> SeriesMask:
        return self.dimension_delimiter.join(
            self.all_values_selected_char
            if dimension.total_num_values == len(dimension.selected_values)
            else self.dimension_value_delimiter.join(value.code for value in dimension.selected_values)
            for dimension in dimensions
        )
