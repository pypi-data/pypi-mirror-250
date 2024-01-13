from abc import ABC, abstractmethod
from collections.abc import Iterator
from typing import Generic, TypeVar

__all__ = ["Serializer"]


T = TypeVar("T")


class Serializer(ABC, Generic[T]):
    @abstractmethod
    def serialize(self, value: T) -> Iterator[bytes]:
        ...
