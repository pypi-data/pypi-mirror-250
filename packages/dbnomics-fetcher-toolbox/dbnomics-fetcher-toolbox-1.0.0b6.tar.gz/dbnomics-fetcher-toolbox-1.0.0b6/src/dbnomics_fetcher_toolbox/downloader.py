import logging
from abc import ABC, abstractmethod
from collections.abc import Iterator
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Final, Literal, TypeVar, overload

import daiquiri
import msgspec
from contexttimer import Timer
from returns.maybe import Maybe, Nothing, Some

from dbnomics_fetcher_toolbox._internal.argparse_utils import AnyId
from dbnomics_fetcher_toolbox._internal.file_utils import (
    create_directory,
    format_file_path_with_size,
    is_directory_empty,
    move_file,
    write_chunks,
)
from dbnomics_fetcher_toolbox._internal.formatting_utils import format_csv_values, format_timer
from dbnomics_fetcher_toolbox._internal.reports import DownloadReport
from dbnomics_fetcher_toolbox.errors.downloader import (
    DuplicateResource,
    DuplicateResourceGroup,
    RequiredResourceSkipped,
)
from dbnomics_fetcher_toolbox.parsers.base import FileParser
from dbnomics_fetcher_toolbox.resource import Resource
from dbnomics_fetcher_toolbox.resource_group import ResourceGroup
from dbnomics_fetcher_toolbox.sources.base import Source
from dbnomics_fetcher_toolbox.types import ResourceFullId, ResourceGroupId, ResourceId, ResourceUpdates

if TYPE_CHECKING:
    from dbnomics_fetcher_toolbox.serializers.base import Serializer

__all__ = ["Downloader"]


logger = daiquiri.getLogger(__name__)


DEFAULT_CACHE_DIR_NAME: Final = ".cache"
DEFAULT_DEBUG_DIR_NAME: Final = ".debug"
DEFAULT_STATE_DIR_NAME: Final = ".state"

RESOURCE_UPDATES_FILE_NAME: Final = "resource_updates.json"


T = TypeVar("T")


class Downloader(ABC):
    def __init__(
        self,
        *,
        cache_dir: Path | None = None,
        debug_dir: Path | None = None,
        excluded: list[AnyId] | None = None,
        fail_fast: bool = False,
        incremental: bool = True,
        limit: int | None = None,
        report_file: Path | None = None,
        resume_mode: bool = True,
        selected: list[AnyId] | None = None,
        state_dir: Path | None = None,
        target_dir: Path,
    ) -> None:
        if cache_dir is None:
            cache_dir = target_dir / Path(DEFAULT_CACHE_DIR_NAME)
        self._cache_dir = cache_dir

        if debug_dir is None:
            debug_dir = target_dir / Path(DEFAULT_DEBUG_DIR_NAME)
        self._debug_dir = debug_dir

        self._excluded = excluded
        self._fail_fast = fail_fast
        self._incremental = incremental
        self._limit = limit
        self._report_file = report_file
        self._resume_mode = resume_mode
        self._selected = selected

        if state_dir is None:
            state_dir = target_dir / Path(DEFAULT_STATE_DIR_NAME)
        self._state_dir = state_dir

        self._target_dir = target_dir

        self._report = DownloadReport()

        self._matched_excluded: set[AnyId] = set()
        self._matched_selected: set[AnyId] = set()

        self._create_directories()

        if self._excluded:
            logger.debug("Will skip processing those resources or groups: %s", format_csv_values(self._excluded))
        if self._selected:
            logger.debug("Will process only those resources or groups: %s", format_csv_values(self._selected))

    def process_group(self, group: ResourceGroup) -> None:
        group_id = group.id

        self._report.register_group_start(group_id)

        # Check duplicate before skipping by options to ensure the error is shown to the user,
        # even if the group is skipped.
        if self._report.is_group_already_processed(group_id):
            logger.error("Resource group %r has already been processed (it is a duplicate), skipping", group_id)
            self._report.register_group_failure(group_id, error=DuplicateResourceGroup(group_id))
            return

        skip_message = self._is_group_skipped_by_options(group_id)
        if skip_message is not None:
            self._report.register_group_skip(group_id, message=skip_message)
            return

        logger.debug("Starting to process resource group %r...", group_id)

        with Timer() as timer:
            try:
                group._start(downloader=self)  # noqa: SLF001
            except Exception as exc:
                self._report.register_group_failure(group_id, error=exc, timer=timer)
                logger.error(  # noqa: TRY400
                    "Error processing resource group %r",
                    group_id,
                    duration=format_timer(timer),
                    exc_info=not self._fail_fast,
                )
                if self._fail_fast:
                    raise
                return

        self._finalize_group(group)
        self._report.register_group_success(group_id, timer=timer)
        logger.info("Resource group %r has been processed successfully", group_id, duration=format_timer(timer))

    @overload
    def process_resource(
        self,
        resource: Resource[T],
        *,
        required: Literal[False] = False,
        serializer: "Serializer[T] | None" = None,
        source: Source,
        updated_at: datetime | None = None,
    ) -> T | None:
        ...

    @overload
    def process_resource(
        self,
        resource: Resource[T],
        *,
        required: Literal[True],
        serializer: "Serializer[T] | None" = None,
        source: Source,
        updated_at: datetime | None = None,
    ) -> T:
        ...

    @overload
    def process_resource(
        self,
        resource: Resource[T],
        *,
        required: bool = False,
        serializer: "Serializer[T] | None" = None,
        source: Source,
        updated_at: datetime | None = None,
    ) -> T | None:
        ...

    def process_resource(
        self,
        resource: Resource[T],
        *,
        required: bool = False,
        serializer: "Serializer[T] | None" = None,
        source: Source,
        updated_at: datetime | None = None,
    ) -> T | None:
        loaded_value = self._process_resource(
            resource, required=required, serializer=serializer, source=source, updated_at=updated_at
        )
        if required:
            return loaded_value.unwrap()
        return loaded_value.value_or(None)

    def start(self) -> None:
        self._resource_updates = self._load_resource_updates()

        try:
            self._process()
        finally:
            self._log_unmatched_filters()
            self._save_report()
            self._save_resource_updates()
            self._log_stats()

    def _create_directories(self) -> None:
        create_directory(self._cache_dir, kind="cache", with_gitignore=True)
        create_directory(self._debug_dir, kind="debug", with_gitignore=True)
        create_directory(self._state_dir, kind="state", with_gitignore=True)
        create_directory(self._target_dir, kind="target")

    def _finalize_group(self, group: "ResourceGroup") -> None:
        if not group._kept_resources:  # noqa: SLF001
            return

        target_files = []
        for resource in group._kept_resources:  # noqa: SLF001
            file = resource.file
            resource_full_id = ResourceFullId.from_group_and_resource(group, resource)
            cache_file = self._cache_dir / file
            target_file = self._target_dir / file
            if self._resume_mode and target_file.is_file():
                logger.debug(
                    "Ignoring file %r of resource %r because it is already in target dir %r",
                    str(file),
                    str(resource_full_id),
                    str(self._target_dir),
                )
                continue
            if not cache_file.is_file():
                logger.error(
                    "Ignoring file %r of resource %r because it does not exist in cache dir %r",
                    str(file),
                    str(resource_full_id),
                    str(self._cache_dir),
                )
                continue

            move_file(cache_file, target_file)
            target_files.append(target_file)

        logger.debug(
            "Moved files of resources of group %r from cache dir to target dir: %s",
            group.id,
            format_csv_values(map(format_file_path_with_size, target_files)),
        )

    def _is_group_skipped_by_options(self, group_id: ResourceGroupId) -> str | None:
        def iter_comparable_ids(any_ids: list[AnyId]) -> Iterator[ResourceId | ResourceGroupId]:
            for any_id in any_ids:
                if isinstance(any_id, ResourceFullId):
                    if any_id.group_id is not None:
                        yield any_id.group_id
                else:
                    yield any_id

        if self._excluded is not None:
            excluded_comparable_ids = iter_comparable_ids(self._excluded)
            if group_id in excluded_comparable_ids:
                self._matched_excluded.add(group_id)
                return f"Skipping group {group_id!r} because it was excluded"

        if self._selected is not None:
            selected_comparable_ids = iter_comparable_ids(self._selected)
            if group_id in selected_comparable_ids:
                self._matched_selected.add(group_id)
            else:
                return f"Skipping group {group_id!r} because it was not selected"

        return None

    def _is_resource_skipped_by_incremental_mode(
        self, resource_full_id: ResourceFullId, *, updated_at: datetime | None
    ) -> str | None:
        if updated_at is None:
            return None

        if self._resource_updates is None:
            return None

        last_updated_at = self._resource_updates.get(resource_full_id)
        if last_updated_at is None:
            return None

        if last_updated_at > updated_at:
            logger.warning(
                "Incremental mode: last update date %r of resource %s is more recent than the new one %r, ignoring invalid value and processing resource",  # noqa: E501
                last_updated_at.isoformat(),
                str(resource_full_id),
                updated_at.isoformat(),
            )
            return None

        if updated_at > last_updated_at:
            logger.debug(
                "Incremental mode: processing resource %r because the new update date %r is more recent than the last one %r",  # noqa: E501
                str(resource_full_id),
                updated_at.isoformat(),
                last_updated_at.isoformat(),
            )
            return None

        assert updated_at == last_updated_at
        return f"Incremental mode: skipping resource {str(resource_full_id)!r} because the last update date is the same as the new one: {updated_at.isoformat()}"  # noqa: E501

    def _is_resource_skipped_by_options(self, resource_full_id: ResourceFullId) -> str | None:
        resource_group_id = resource_full_id.group_id

        if self._excluded is not None:
            excluded_as_str = list(map(str, self._excluded))
            if str(resource_full_id) in excluded_as_str:
                self._matched_excluded.add(resource_full_id)
                return f"Skipping resource {str(resource_full_id)!r} because it was excluded"

            if resource_group_id in excluded_as_str:
                self._matched_excluded.add(resource_full_id)
                return f"Skipping resource {str(resource_full_id)!r} because its group {str(resource_group_id)!r} was excluded"  # noqa: E501

        if self._selected is not None:
            selected_as_str = list(map(str, self._selected))
            if str(resource_full_id) in selected_as_str or resource_group_id in selected_as_str:
                self._matched_selected.add(resource_full_id)
            else:
                return f"Skipping resource {str(resource_full_id)!r} because it was not selected"

        if self._limit is not None and len(self._report.resource_full_ids) == self._limit:
            return f"Skipping resource {str(resource_full_id)!r} because the limit has been reached"

        return None

    def _load_resource(
        self,
        resource: Resource[T],
        *,
        group: "ResourceGroup | None",
        keep: bool,
        resource_full_id: ResourceFullId,
        serializer: "Serializer[T] | None",
        source: Source,
        timer: Timer,
    ) -> T:
        file = resource.file
        cache_file = self._cache_dir / file
        target_file = self._target_dir / file

        # Ensure that file's parent directory exists, in case file contains a sub-directory.
        cache_file.parent.mkdir(exist_ok=True, parents=True)

        output_file: Path

        if self._resume_mode and target_file.is_file():
            output_file = target_file
            resume_message = f"Resume mode: reloading existing file of resource {str(resource_full_id)!r} from target dir: {format_file_path_with_size(target_file)}"  # noqa: E501
            logger.debug(resume_message)
            loaded_value = resource.parser.parse_file(target_file)
            self._report.register_resource_skip(resource_full_id, message=resume_message)
        else:
            output_file = cache_file

            if self._resume_mode and cache_file.is_file():
                resume_message = f"Resume mode: reloading existing file of resource {str(resource_full_id)!r} from cache dir: {format_file_path_with_size(cache_file)}"  # noqa: E501
                logger.debug(resume_message)
                loaded_value = resource.parser.parse_file(cache_file)
            else:
                logger.debug("Loading resource content from source %r...", type(source).__qualname__)
                with Timer() as timer:
                    loaded_value = self._load_source(
                        output_file=cache_file,
                        parser=resource.parser,
                        resource_full_id=resource_full_id,
                        serializer=serializer,
                        source=source,
                    )
                logger.debug(
                    "Loaded resource content from source successfully to %s",
                    format_file_path_with_size(cache_file),
                    duration=format_timer(timer),
                )

            if keep:
                if group:
                    group._kept_resources.append(resource)  # noqa: SLF001
                else:
                    move_file(cache_file, target_file)
                    logger.debug(
                        "Moved file of resource %r from cache dir to target dir because keep=True: %s",
                        str(resource_full_id),
                        format_file_path_with_size(target_file),
                    )
                    output_file = target_file

            self._report.register_resource_success(resource_full_id, output_file=output_file, timer=timer)
            logger.info(
                "Resource %r has been processed successfully and written to %s",
                str(resource_full_id),
                format_file_path_with_size(output_file),
                duration=format_timer(timer),
            )

        return loaded_value

    def _load_resource_updates(self) -> ResourceUpdates | None:
        if not self._incremental:
            logger.debug("Incremental mode is disabled because of downloader option")
            return None

        resource_updates_file = self._resource_updates_file
        if not resource_updates_file.is_file():
            logger.debug("Incremental mode is disabled because %s does not exist", str(resource_updates_file))
            return None

        resource_updates_content = resource_updates_file.read_bytes()
        resource_updates_data = msgspec.json.decode(resource_updates_content, type=dict[str, datetime])
        resource_updates = {ResourceFullId.parse(k): updated_at for k, updated_at in resource_updates_data.items()}
        logger.debug(
            "Loaded resource updates from %s, enabling incremental mode",
            format_file_path_with_size(resource_updates_file),
        )
        return resource_updates

    def _load_source(
        self,
        output_file: Path,
        parser: FileParser[T],
        resource_full_id: ResourceFullId,
        serializer: "Serializer[T] | None",
        source: Source,
    ) -> T:
        source_class_name = source.__class__.__name__
        source_debug_dir = self._debug_dir / source_class_name
        source_debug_dir.mkdir(exist_ok=True)
        source_content = source.iter_bytes(debug_dir=source_debug_dir, resource_full_id=resource_full_id)
        loaded_value = self._parse_source_content(
            source_content, output_file=output_file, parser=parser, serializer=serializer
        )
        if is_directory_empty(source_debug_dir):
            source_debug_dir.rmdir()
        return loaded_value

    def _log_stats(self) -> None:
        logger.info(self._report.build_stats())

    def _log_unmatched_filters(self) -> None:
        def as_str(values: set[AnyId]) -> set[str]:
            return {str(value) for value in values}

        if self._excluded is not None and (
            unmatched_excluded := as_str(set(self._excluded)) - as_str(self._matched_excluded)
        ):
            logger.warning(
                "Some excluded resources or groups were never processed: %s",
                format_csv_values(unmatched_excluded),
            )

        if self._selected is not None and (
            unmatched_selected := as_str(set(self._selected)) - as_str(self._matched_selected)
        ):
            logger.warning(
                "Some selected resources or groups were never processed: %s",
                format_csv_values(unmatched_selected),
            )

    def _parse_source_content(
        self,
        source_content: Iterator[bytes],
        *,
        output_file: Path,
        parser: "FileParser[T]",
        serializer: "Serializer[T] | None",
    ) -> T:
        if serializer is None:
            serializer = parser.default_serializer

        if serializer is None:
            write_chunks(source_content, output_file=output_file)
            return parser.parse_file(output_file)

        raw_output_file = output_file.with_suffix(f"{output_file.suffix}.raw")
        write_chunks(source_content, output_file=raw_output_file)

        parsed_value = parser.parse_file(raw_output_file)

        serialized_value = serializer.serialize(parsed_value)
        write_chunks(serialized_value, output_file=output_file)

        raw_output_file.unlink()

        return parsed_value

    @abstractmethod
    def _process(self) -> None:
        ...

    def _process_group_resource(
        self,
        resource: Resource[T],
        *,
        group: "ResourceGroup",
        keep: bool,
        required: bool,
        serializer: "Serializer[T] | None",
        source: Source,
        updated_at: datetime | None = None,
    ) -> T | None:
        loaded_value = self._process_resource(
            resource,
            group=group,
            keep=keep,
            required=required,
            serializer=serializer,
            source=source,
            updated_at=updated_at,
        )
        if required:
            return loaded_value.unwrap()
        return loaded_value.value_or(None)

    def _process_resource(
        self,
        resource: Resource[T],
        *,
        group: "ResourceGroup | None" = None,
        keep: bool = True,
        required: bool,
        serializer: "Serializer[T] | None",
        source: Source,
        updated_at: datetime | None = None,
    ) -> Maybe[T]:
        if updated_at is not None and updated_at.tzinfo is None:
            msg = "updated_at datetime must be timezone-aware"
            raise ValueError(msg)

        resource_full_id = ResourceFullId.from_group_and_resource(group, resource)

        self._report.register_resource_start(resource_full_id)

        # Check duplicate before skipping by options to ensure the error is shown to the user,
        # even if the resource is skipped.
        if self._report.is_resource_already_processed(resource_full_id):
            logger.error("Resource %r has already been processed (it is a duplicate), skipping", str(resource_full_id))
            error = DuplicateResource(resource_full_id)
            self._report.register_resource_failure(resource_full_id, error=error)
            if not required:
                return Nothing
            raise RequiredResourceSkipped(group=group, resource=resource) from error

        skip_message = self._is_resource_skipped_by_options(resource_full_id)
        if skip_message is not None:
            if required:
                logger.debug("Don't skip resource %r because it is required", str(resource_full_id))
            else:
                self._report.register_resource_skip(resource_full_id, message=skip_message)
                return Nothing

        skip_message = self._is_resource_skipped_by_incremental_mode(resource_full_id, updated_at=updated_at)
        if skip_message is not None:
            logger.debug(skip_message)
            self._report.register_resource_skip(resource_full_id, message=skip_message)
            return Nothing

        logger.debug("Starting to process resource %r...", str(resource_full_id))

        with Timer() as timer:
            try:
                loaded_value = self._load_resource(
                    resource,
                    group=group,
                    keep=keep,
                    resource_full_id=resource_full_id,
                    serializer=serializer,
                    source=source,
                    timer=timer,
                )
            except Exception as exc:
                logger.log(
                    logging.ERROR if required else logging.WARNING,
                    "Error processing %s resource %r",
                    "required" if required else "non-required",
                    str(resource_full_id),
                    duration=format_timer(timer),
                    exc_info=not self._fail_fast,
                )
                if required:
                    self._report.register_resource_failure(resource_full_id, error=exc, timer=timer)
                if self._fail_fast or required:
                    raise
                return Nothing

        if updated_at is not None:
            if self._resource_updates is None:
                self._resource_updates = {}
            self._resource_updates[resource_full_id] = updated_at

        return Some(loaded_value)

    @property
    def _resource_updates_file(self) -> Path:
        return self._state_dir / RESOURCE_UPDATES_FILE_NAME

    def _save_report(self) -> None:
        report_file = self._report_file
        if report_file is None:
            logger.debug("Skip saving the download report because no report file has been given")
            return

        report_file.write_bytes(self._report.dump_as_json_bytes())
        logger.info("Download report saved to %s", format_file_path_with_size(report_file))

    def _save_resource_updates(self) -> None:
        resource_updates = self._resource_updates
        if resource_updates is None:
            return

        resource_updates_file = self._resource_updates_file
        resource_updates_data = {
            str(resource_full_id): updated_at for resource_full_id, updated_at in resource_updates.items()
        }
        resource_updates_content = msgspec.json.format(msgspec.json.encode(resource_updates_data))
        resource_updates_file.write_bytes(resource_updates_content)
        logger.info("Resource updates saved to %s", format_file_path_with_size(resource_updates_file))
