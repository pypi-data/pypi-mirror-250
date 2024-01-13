import hashlib

from dbnomics_data_model.json_utils import serialize_json

from dbnomics_fetcher_toolbox.bisect.partitions.dimension.___model import BisectDimension
from dbnomics_fetcher_toolbox.bisect.partitions.dimension.__types import PartitionId


def hash_dimensions(dimensions: list[BisectDimension]) -> PartitionId:
    return hashlib.sha1(serialize_json(dimensions)).hexdigest()  # noqa: S324
