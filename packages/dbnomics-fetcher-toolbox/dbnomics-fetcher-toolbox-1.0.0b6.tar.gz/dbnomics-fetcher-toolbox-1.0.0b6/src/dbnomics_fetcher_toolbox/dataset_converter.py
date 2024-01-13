from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, TypeVar

from dbnomics_data_model.model import DatasetCode, DatasetId, ProviderCode

from dbnomics_fetcher_toolbox.resource import Resource

if TYPE_CHECKING:
    from dbnomics_data_model.storage import Storage, StorageSession

    from dbnomics_fetcher_toolbox.converter import Converter


__all__ = ["DatasetConverter"]


T = TypeVar("T")


class DatasetConverter(ABC):
    def __init__(self, *, dataset_id: DatasetId | str) -> None:
        if isinstance(dataset_id, str):
            dataset_id = DatasetId.parse(dataset_id)
        self.dataset_id = dataset_id

    @property
    def dataset_code(self) -> DatasetCode:
        return self.dataset_id.dataset_code

    def load_resource(self, resource: Resource[T]) -> T:
        return self._converter.load_resource(resource)

    @property
    def provider_code(self) -> ProviderCode:
        return self.dataset_id.provider_code

    @property
    def storage(self) -> "Storage":
        return self._session.storage

    @abstractmethod
    def _process(self) -> None:
        ...

    def _start(self, *, converter: "Converter", session: "StorageSession") -> None:
        self._converter = converter
        self._session = session
        self._process()
