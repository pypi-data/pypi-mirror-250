from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from datetime import datetime, timezone
from itertools import groupby
from pathlib import Path
from typing import Any, Literal, TypeAlias

from contexttimer import Timer
from dbnomics_data_model.json_utils import dump_as_json_bytes
from dbnomics_data_model.json_utils.typedload_utils import add_handler
from typedload.datadumper import Dumper

from dbnomics_fetcher_toolbox._internal.reports.error_chain import build_error_chain
from dbnomics_fetcher_toolbox.types import ResourceFullId, ResourceGroupId, ResourceId

from .status import Failure, Skip, Success

__all__ = ["DownloadReport"]


TypedloadHandler: TypeAlias = tuple[Callable[[Any], bool], Callable[[Dumper, Any, type], Any]]


@dataclass(kw_only=True)
class ResourceSuccess(Success):
    output_file: Path


ResourceStatus: TypeAlias = Failure | Skip | ResourceSuccess

GroupStatus: TypeAlias = Failure | Skip | Success


@dataclass(kw_only=True)
class ResourceReport:
    group_id: ResourceGroupId | None = field(default=None, init=False)
    resource_full_id: ResourceFullId
    resource_id: ResourceId = field(default=ResourceId.parse("empty"), init=False)
    started_at: datetime
    status: ResourceStatus
    type: Literal["resource"] = field(default="resource")

    def __post_init__(self) -> None:
        self.group_id = self.resource_full_id.group_id
        self.resource_id = self.resource_full_id.resource_id


@dataclass(kw_only=True)
class GroupReport:
    group_id: ResourceGroupId
    started_at: datetime
    status: GroupStatus
    type: Literal["resource_group"] = field(default="resource_group")


@dataclass(kw_only=True)
class ReportStats:
    groups: dict[str, int]
    resources: dict[str, int]


GroupOrResourceReport: TypeAlias = ResourceReport | GroupReport


class DownloadReport:
    def __init__(self) -> None:
        self.items: list[GroupOrResourceReport] = []

        self._group_starts: dict[ResourceGroupId, datetime] = {}
        self._resource_starts: dict[ResourceFullId, datetime] = {}

    def build_stats(self) -> "ReportStats":
        def by_status_type(item: GroupOrResourceReport) -> str:
            return item.status.type

        def get_count_by_status(items: Sequence[GroupOrResourceReport]) -> dict[str, int]:
            return {k: len(list(v)) for k, v in groupby(sorted(items, key=by_status_type), key=by_status_type)}

        groups = {"total": len(self.group_ids)} | get_count_by_status(self.groups)
        resources = {"total": len(self.resource_full_ids)} | get_count_by_status(self.resources)
        return ReportStats(groups=groups, resources=resources)

    def dump_as_json_bytes(self) -> bytes:
        dumper = self._create_dumper()
        data = {"items": self.items}
        return dump_as_json_bytes(data, dumper=dumper)

    @property
    def group_ids(self) -> list[ResourceGroupId]:
        return [report_item.group_id for report_item in self.items if isinstance(report_item, GroupReport)]

    @property
    def groups(self) -> list["GroupReport"]:
        return [report_item for report_item in self.items if isinstance(report_item, GroupReport)]

    def is_group_already_processed(self, group_id: ResourceGroupId) -> bool:
        return group_id in self.group_ids

    def is_resource_already_processed(self, resource_full_id: ResourceFullId) -> bool:
        return resource_full_id in self.resource_full_ids

    def register_group_failure(
        self, group_id: ResourceGroupId, *, error: Exception, timer: Timer | None = None
    ) -> None:
        self.items.append(
            GroupReport(
                group_id=group_id,
                started_at=self._group_starts[group_id],
                status=Failure(duration=None if timer is None else timer.elapsed, error=error),
            )
        )

    def register_group_skip(self, group_id: ResourceGroupId, *, message: str) -> None:
        self.items.append(
            GroupReport(
                group_id=group_id,
                started_at=self._group_starts[group_id],
                status=Skip(message=message),
            )
        )

    def register_group_start(self, group_id: ResourceGroupId) -> None:
        self._group_starts[group_id] = datetime.now(tz=timezone.utc)

    def register_group_success(self, group_id: ResourceGroupId, *, timer: Timer) -> None:
        self.items.append(
            GroupReport(
                group_id=group_id,
                started_at=self._group_starts[group_id],
                status=Success(duration=timer.elapsed),
            )
        )

    def register_resource_failure(
        self, resource_full_id: ResourceFullId, *, error: Exception, timer: Timer | None = None
    ) -> None:
        self.items.append(
            ResourceReport(
                resource_full_id=resource_full_id,
                started_at=self._resource_starts[resource_full_id],
                status=Failure(duration=None if timer is None else timer.elapsed, error=error),
            )
        )

    def register_resource_skip(self, resource_full_id: ResourceFullId, *, message: str) -> None:
        self.items.append(
            ResourceReport(
                resource_full_id=resource_full_id,
                started_at=self._resource_starts[resource_full_id],
                status=Skip(message=message),
            )
        )

    def register_resource_start(self, resource_full_id: ResourceFullId) -> None:
        self._resource_starts[resource_full_id] = datetime.now(tz=timezone.utc)

    def register_resource_success(self, resource_full_id: ResourceFullId, *, output_file: Path, timer: Timer) -> None:
        self.items.append(
            ResourceReport(
                resource_full_id=resource_full_id,
                started_at=self._resource_starts[resource_full_id],
                status=ResourceSuccess(duration=timer.elapsed, output_file=output_file),
            )
        )

    @property
    def resource_full_ids(self) -> list[ResourceFullId]:
        return [report_item.resource_full_id for report_item in self.items if isinstance(report_item, ResourceReport)]

    @property
    def resources(self) -> list["ResourceReport"]:
        return [report_item for report_item in self.items if isinstance(report_item, ResourceReport)]

    def _create_dumper(self) -> Dumper:
        dumper = Dumper(hidedefault=False, isodates=True)
        add_handler(
            dumper,
            (
                lambda x: isinstance(x, ResourceFullId),
                lambda _dumper, value, _value_type: str(value),
            ),
            sample_value=ResourceFullId.parse("R1"),
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
