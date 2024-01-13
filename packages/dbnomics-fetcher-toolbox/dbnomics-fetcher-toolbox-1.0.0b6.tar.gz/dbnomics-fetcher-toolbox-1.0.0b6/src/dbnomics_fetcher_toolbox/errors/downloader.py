from pathlib import Path
from typing import TYPE_CHECKING, Any

from dbnomics_fetcher_toolbox._internal.file_utils import format_file_path_with_size
from dbnomics_fetcher_toolbox.types import ResourceFullId

from .base import FetcherToolboxError

if TYPE_CHECKING:
    from dbnomics_fetcher_toolbox import Resource
    from dbnomics_fetcher_toolbox.resource_group import ResourceGroup
    from dbnomics_fetcher_toolbox.types import ResourceGroupId


class DownloaderError(FetcherToolboxError):
    pass


class DirectoryCreateError(DownloaderError):
    def __init__(self, directory: Path, *, kind: str) -> None:
        msg = f"Could not create the {kind} directory {str(directory)!r}"
        super().__init__(msg=msg)
        self.directory = directory
        self.kind = kind


class DuplicateResource(DownloaderError):
    def __init__(self, resource_full_id: "ResourceFullId") -> None:
        msg = f"The resource {str(resource_full_id)!r} has already been processed. Resource full IDs must be unique."
        super().__init__(msg=msg)
        self.resource_id = resource_full_id


class DuplicateResourceGroup(DownloaderError):
    def __init__(self, group_id: "ResourceGroupId") -> None:
        msg = f"The resource group {group_id!r} has already been processed. Resource group full ID must be unique."
        super().__init__(msg=msg)
        self.group_id = group_id


class GroupProcessError(DownloaderError):
    def __init__(self, *, group: "ResourceGroup") -> None:
        msg = f"Error processing group {group.id!r}"
        super().__init__(msg=msg)
        self.group = group


class ResourceBytesParseError(DownloaderError):
    def __init__(self, *, content: bytes) -> None:
        msg = "Error parsing the resource bytes"
        super().__init__(msg=msg)
        self.content = content


class ResourceBytesValidationError(DownloaderError):
    def __init__(self, *, content: bytes) -> None:
        msg = "Error validating the resource bytes"
        super().__init__(msg=msg)
        self.content = content


class ResourceFileParseError(DownloaderError):
    def __init__(self, *, file: Path) -> None:
        msg = f"Error parsing the resource file {format_file_path_with_size(file)}"
        super().__init__(msg=msg)
        self.file = file


class ResourceFileValidationError(DownloaderError):
    def __init__(self, *, file: Path) -> None:
        msg = f"Error validating the resource file {format_file_path_with_size(file)}"
        super().__init__(msg=msg)
        self.file = file


class ResourceError(FetcherToolboxError):
    def __init__(self, *, group: "ResourceGroup | None", msg: str, resource: "Resource[Any]") -> None:
        super().__init__(msg=msg)
        resource_full_id = ResourceFullId.from_group_and_resource(group, resource)
        self.group = group
        self.resource = resource
        self.resource_full_id = resource_full_id


class RequiredResourceSkipped(ResourceError):
    def __init__(self, *, group: "ResourceGroup | None", resource: "Resource[Any]") -> None:
        resource_full_id = ResourceFullId.from_group_and_resource(group, resource)
        msg = f"Required resource {str(resource_full_id)!r} was skipped"
        super().__init__(group=group, msg=msg, resource=resource)
