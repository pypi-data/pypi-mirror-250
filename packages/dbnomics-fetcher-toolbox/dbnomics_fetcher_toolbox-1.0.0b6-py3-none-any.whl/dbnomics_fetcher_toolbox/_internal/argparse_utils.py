import contextlib
from argparse import ArgumentTypeError
from collections.abc import Callable, Iterator
from typing import TypeAlias, TypeVar, cast

from dbnomics_data_model.model import DatasetCode
from dbnomics_data_model.model.identifiers.errors import DatasetCodeParseError

from dbnomics_fetcher_toolbox.types import ResourceFullId, ResourceGroupId, ResourceId

TNumber = TypeVar("TNumber", int, float)

AnyId: TypeAlias = ResourceId | ResourceGroupId | ResourceFullId


def any_id(value: str) -> AnyId:
    for parse in [ResourceId.parse, ResourceGroupId.parse, ResourceFullId.parse]:
        with contextlib.suppress(TypeError):
            return cast(AnyId, parse(value))

    msg = f"{value!r} is not a valid resource ID, group ID or resource full ID"
    raise ArgumentTypeError(msg)


def csv_any_ids(value: str) -> list[AnyId]:
    items = csv_str(value)
    return [any_id(item) for item in items]


def csv_dataset_codes(value: str) -> list[DatasetCode]:
    items = csv_str(value)
    return [dataset_code(item) for item in items]


def csv_str(value: str) -> list[str]:
    """Transform a string containing comma-separated values to a list of strings.

    If the input string has spaces around commas, they are removed.

    >>> csv_str('')
    []
    >>> csv_str('a')
    ['a']
    >>> csv_str('a,b')
    ['a', 'b']
    """

    def iter_parts(parts: list[str]) -> Iterator[str]:
        for part in parts:
            part = part.strip()  # noqa: PLW2901
            if not part:
                msg = f"Invalid input: {value}"
                raise ArgumentTypeError(msg)
            yield part

    if not value:
        return []
    return list(iter_parts(value.split(",")))


def dataset_code(value: str) -> DatasetCode:
    try:
        return DatasetCode.parse(value)
    except DatasetCodeParseError as exc:
        msg = f"{value!r} is not a valid dataset code"
        raise ArgumentTypeError(msg) from exc


def positive(numeric_type: type[TNumber]) -> Callable[[str], TNumber]:
    def require_positive(value: str) -> TNumber:
        number = numeric_type(value)
        if number <= 0:
            msg = f"{value!r} is not a positive number"
            raise ArgumentTypeError(msg)
        return number

    return require_positive
