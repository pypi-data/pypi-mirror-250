from dbnomics_data_model.model import DatasetCode

from .base import FetcherToolboxError


class ConverterError(FetcherToolboxError):
    pass


class DuplicateDataset(ConverterError):
    def __init__(self, dataset_code: DatasetCode) -> None:
        msg = f"The dataset {str(dataset_code)!r} has already been processed. Dataset codes must be unique."
        super().__init__(msg=msg)
        self.dataset_code = dataset_code
