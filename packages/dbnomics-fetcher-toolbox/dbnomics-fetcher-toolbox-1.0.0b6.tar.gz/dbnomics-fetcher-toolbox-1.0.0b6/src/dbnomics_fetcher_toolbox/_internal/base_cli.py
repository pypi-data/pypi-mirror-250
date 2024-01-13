import argparse
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Final, NoReturn, Self, TypeVar, cast

from environs import Env

from dbnomics_fetcher_toolbox._internal.argparse_utils import csv_str
from dbnomics_fetcher_toolbox._internal.logging_utils import setup_logging

EXCLUDE_OPTION_NAME: Final = "--exclude"
LIMIT_OPTION_NAME: Final = "--limit"
ONLY_OPTION_NAME: Final = "--only"


@dataclass(frozen=True, kw_only=True)
class BaseCLIArgs(ABC):
    fail_fast: bool
    log_format: str | None
    log_levels: list[str] | None
    resume: bool

    @classmethod
    @abstractmethod
    def parse(cls, *, package_name: str) -> Self:
        ...


TCLIArgs = TypeVar("TCLIArgs", bound=BaseCLIArgs)


class BaseCLIArgsParser:
    def __init__(self, *, args_class: type[TCLIArgs], env: Env | None = None) -> None:
        self.args_class = args_class

        if env is None:
            env = self.create_env_reader()
        self.env = env

        self._argparse_parser = self.create_argparse_parser()

    def create_env_reader(self) -> Env:
        env = Env()
        # read .env file, if it exists, in the current directory (where the user runs the fetcher)
        env.read_env(".env")
        return env

    def create_argparse_parser(self) -> argparse.ArgumentParser:
        argparse_parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        self.setup_argparse_parser(argparse_parser)
        return argparse_parser

    def fail(self, *, msg: str) -> NoReturn:
        self._argparse_parser.error(msg)

    def parse_args_namespace(self, *, package_name: str) -> argparse.Namespace:
        args = self._argparse_parser.parse_args()
        base_cli_args = cast(BaseCLIArgs, args)
        setup_logging(
            log_format=base_cli_args.log_format, log_levels=base_cli_args.log_levels, package_name=package_name
        )
        return args

    def setup_argparse_parser(self, argparse_parser: argparse.ArgumentParser) -> None:
        argparse_parser.add_argument(
            "--fail-fast",
            action="store_true",
            help="exit on first exception instead of just logging it",
        )
        argparse_parser.add_argument(
            "--log-format",
            default=self.env("TOOLBOX_LOG_FORMAT", None),
            type=str,
            help="format of the log messages",
        )
        argparse_parser.add_argument(
            "--log-levels",
            default=self.env("TOOLBOX_LOG_LEVELS", None),
            type=csv_str,
            help="Logging levels: logger_name1=log_level1,logger_name2=log_level2[,...]",
        )
        argparse_parser.add_argument(
            "--resume",
            action=argparse.BooleanOptionalAction,
            default=self.env.bool("TOOLBOX_RESUME_MODE", default=True),
            help="skip already downloaded resources",
        )
