from collections.abc import Iterator
from typing import TYPE_CHECKING, cast

from lxml import etree

from dbnomics_fetcher_toolbox.serializers.base import Serializer

if TYPE_CHECKING:
    from lxml.etree import _ElementTree


__all__ = ["LxmlSerializer"]


class LxmlSerializer(Serializer["_ElementTree"]):
    def __init__(self, *, encoding: str | None = None, pretty_print: bool = True, xml_declaration: bool = True) -> None:
        if encoding is None:
            encoding = "utf-8"
        self.encoding = encoding

        self.pretty_print = pretty_print
        self.xml_declaration = xml_declaration

    def serialize(self, value: "_ElementTree") -> Iterator[bytes]:
        yield cast(
            bytes,
            etree.tostring(
                value, encoding=self.encoding, pretty_print=self.pretty_print, xml_declaration=self.xml_declaration
            ),
        )
