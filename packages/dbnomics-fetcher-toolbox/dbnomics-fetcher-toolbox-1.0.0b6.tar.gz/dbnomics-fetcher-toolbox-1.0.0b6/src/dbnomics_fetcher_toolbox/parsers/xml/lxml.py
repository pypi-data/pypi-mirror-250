from pathlib import Path
from typing import TYPE_CHECKING

from lxml import etree

from dbnomics_fetcher_toolbox.parsers.base import FileParser
from dbnomics_fetcher_toolbox.serializers.base import Serializer
from dbnomics_fetcher_toolbox.serializers.xml import LxmlSerializer

if TYPE_CHECKING:
    from lxml.etree import _ElementTree

__all__ = ["LxmlFileParser"]


class LxmlFileParser(FileParser["_ElementTree"]):
    def __init__(self, *, encoding: str | None = None) -> None:
        if encoding is None:
            encoding = "utf-8"
        self.encoding = encoding

    @property
    def default_serializer(self) -> Serializer["_ElementTree"]:
        return LxmlSerializer()

    def _parse_file(self, input_file: Path) -> "_ElementTree":
        return etree.parse(input_file)
