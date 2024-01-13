import statistics

from dbnomics_fetcher_toolbox.bisect.partitions.dimension.___model import BisectDimension
from dbnomics_fetcher_toolbox.bisect.partitions.dimension.__types import BisectDimensionCode


def select_median_low(dimensions: list[BisectDimension]) -> BisectDimensionCode:
    """Select the dimension having the "median low" number of values.

    To avoid both:

    * the one with the least values because it has a higher probability to return too many results
    * the one with the most values because it could lead to a too long URL
    """
    return statistics.median_low((len(dimension.selected_values), dimension.code) for dimension in dimensions)[1]
