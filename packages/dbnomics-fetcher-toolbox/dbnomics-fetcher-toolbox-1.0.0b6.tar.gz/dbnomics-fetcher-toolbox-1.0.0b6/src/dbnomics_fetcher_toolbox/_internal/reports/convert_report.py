from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime, timezone
from itertools import groupby
from typing import TypeAlias

from contexttimer import Timer
from dbnomics_data_model.json_utils import dump_as_json_bytes
from dbnomics_data_model.json_utils.typedload_utils import add_handler
from dbnomics_data_model.model import DatasetCode
from typedload.datadumper import Dumper

from dbnomics_fetcher_toolbox._internal.reports.error_chain import build_error_chain

from .status import Failure, Skip, Success

__all__ = ["ConvertReport"]


DatasetStatus: TypeAlias = Failure | Skip | Success


@dataclass(kw_only=True)
class DatasetReport:
    dataset_code: DatasetCode
    started_at: datetime
    status: DatasetStatus


@dataclass(kw_only=True)
class ReportStats:
    datasets: dict[str, int]


class ConvertReport:
    def __init__(self) -> None:
        self.datasets: list[DatasetReport] = []

        self._dataset_starts: dict[DatasetCode, datetime] = {}

    def build_stats(self) -> ReportStats:
        def by_status_type(item: DatasetReport) -> str:
            return item.status.type

        def get_count_by_status(items: Sequence[DatasetReport]) -> dict[str, int]:
            return {k: len(list(v)) for k, v in groupby(sorted(items, key=by_status_type), key=by_status_type)}

        datasets = {"total": len(self.dataset_codes)} | get_count_by_status(self.datasets)
        return ReportStats(datasets=datasets)

    @property
    def dataset_codes(self) -> list[DatasetCode]:
        return [dataset_report.dataset_code for dataset_report in self.datasets]

    def dump_as_json_bytes(self) -> bytes:
        dumper = self._create_dumper()
        data = {"datasets": self.datasets}
        return dump_as_json_bytes(data, dumper=dumper)

    def is_dataset_already_processed(self, dataset_code: DatasetCode) -> bool:
        return dataset_code in self.dataset_codes

    def register_dataset_failure(
        self, dataset_code: DatasetCode, *, error: Exception, timer: Timer | None = None
    ) -> None:
        self.datasets.append(
            DatasetReport(
                dataset_code=dataset_code,
                started_at=self._dataset_starts[dataset_code],
                status=Failure(duration=None if timer is None else timer.elapsed, error=error),
            )
        )

    def register_dataset_skip(self, dataset_code: DatasetCode, *, message: str) -> None:
        self.datasets.append(
            DatasetReport(
                dataset_code=dataset_code,
                started_at=self._dataset_starts[dataset_code],
                status=Skip(message=message),
            )
        )

    def register_dataset_start(self, dataset_code: DatasetCode) -> None:
        self._dataset_starts[dataset_code] = datetime.now(tz=timezone.utc)

    def register_dataset_success(self, dataset_code: DatasetCode, *, timer: Timer) -> None:
        self.datasets.append(
            DatasetReport(
                dataset_code=dataset_code,
                started_at=self._dataset_starts[dataset_code],
                status=Success(duration=timer.elapsed),
            )
        )

    def _create_dumper(self) -> Dumper:
        dumper = Dumper(hidedefault=False, isodates=True)
        add_handler(
            dumper,
            (
                lambda x: isinstance(x, DatasetCode),
                lambda _dumper, value, _value_type: str(value),
            ),
            sample_value=DatasetCode.parse("D1"),
        )
        add_handler(
            dumper,
            (
                lambda x: isinstance(x, BaseException),
                lambda _dumper, value, _value_type: build_error_chain(value),
            ),
            sample_value=Exception("test"),
        )
        return dumper
