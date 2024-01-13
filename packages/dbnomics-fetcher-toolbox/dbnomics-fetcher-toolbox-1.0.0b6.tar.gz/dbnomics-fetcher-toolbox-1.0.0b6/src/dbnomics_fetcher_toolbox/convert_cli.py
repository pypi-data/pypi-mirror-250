import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Self

import daiquiri
from dbnomics_data_model.model import DatasetCode
from dbnomics_data_model.storage import StorageUri, parse_storage_uri_or_dir
from dbnomics_data_model.storage.errors.storage_uri import StorageUriParseError

from dbnomics_fetcher_toolbox._internal.argparse_utils import csv_dataset_codes, positive

from ._internal.base_cli import (
    EXCLUDE_OPTION_NAME,
    LIMIT_OPTION_NAME,
    ONLY_OPTION_NAME,
    BaseCLIArgs,
    BaseCLIArgsParser,
)

__all__ = ["ConvertCLIArgs", "ConvertCLIArgsParser"]


logger = daiquiri.getLogger(__package__)


@dataclass(frozen=True, kw_only=True)
class ConvertCLIArgs(BaseCLIArgs):
    exclude: list[DatasetCode]
    limit: int | None
    only: list[DatasetCode]
    report_file: Path | None
    source_dir: Path
    target_storage_uri_or_dir: StorageUri | Path

    @classmethod
    def parse(cls, *, package_name: str) -> Self:
        parser = ConvertCLIArgsParser(args_class=cls)
        args_namespace = parser.parse_args_namespace(package_name=package_name)
        try:
            args_namespace.target_storage_uri_or_dir = parse_storage_uri_or_dir(
                args_namespace.target_storage_uri_or_dir
            )
        except StorageUriParseError as exc:
            parser.fail(msg=str(exc))

        return cls(**vars(args_namespace))

    def as_converter_kwargs(self) -> dict[str, Any]:
        return {
            "excluded": self.exclude,
            "fail_fast": self.fail_fast,
            "limit": self.limit,
            "report_file": self.report_file,
            "resume_mode": self.resume,
            "selected": self.only,
            "source_dir": self.source_dir,
            "target_storage_uri_or_dir": self.target_storage_uri_or_dir,
        }


class ConvertCLIArgsParser(BaseCLIArgsParser):
    def setup_argparse_parser(self, argparse_parser: argparse.ArgumentParser) -> None:
        super().setup_argparse_parser(argparse_parser)

        argparse_parser.add_argument("source_dir", type=Path, help="directory where provider data is read from")
        argparse_parser.add_argument(
            "target_storage_uri_or_dir",
            help="URI of the storage adapter used to write converted data, or a directory",
            type=str,
        )

        argparse_parser.add_argument(
            LIMIT_OPTION_NAME,
            default=self.env("TOOLBOX_CONVERT_LIMIT", None),
            help="build a maximum number of datasets",
            type=positive(int),
        )
        argparse_parser.add_argument(
            "--report-file",
            default=self.env("TOOLBOX_CONVERT_REPORT_FILE", "convert_report.json"),
            help="output file to write the error report to",
            type=Path,
        )

        dataset_selection = argparse_parser.add_mutually_exclusive_group()
        dataset_selection.add_argument(
            EXCLUDE_OPTION_NAME,
            default=self.env("TOOLBOX_CONVERT_EXCLUDE", None),
            help="do not convert the specified datasets",
            metavar="DATASET_CODES",
            type=csv_dataset_codes,
        )
        dataset_selection.add_argument(
            ONLY_OPTION_NAME,
            default=self.env("TOOLBOX_CONVERT_ONLY", None),
            help="convert only the specified datasets",
            metavar="DATASET_CODES",
            type=csv_dataset_codes,
        )
