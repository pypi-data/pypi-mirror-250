from enum import Enum

from ..block.link import Link
from ..element import BlockElement, ElementList
from ..inline.code import Code
from ..inline.emphasis import Bold, BoldItalic, Italic

TableElement = str, Link, Code, Bold, Italic, BoldItalic


class Alignment(Enum):
    LEFT = ":---"
    RIGHT = "---:"
    CENTER = ":---:"
    DEFAULT = "---"


class Table(BlockElement):
    """The Table element

    Every cell's content can be str, Link, Code, Bold, Italic or BoldItalic

    Attributes:
        headers: a list of the header, which can be any type in TableElement
        content: a list of every row's content
        alignments: a list of every columns' alignment
    """

    def __init__(self,
                 header: list[TableElement],
                 content: list[list[TableElement]],
                 alignment: list[Alignment] = []) -> None:
        super().__init__()
        self.headers = ElementList(tuple(header))
        self.contents = [ElementList(row) for row in content]
        self.alignments = alignment

        self.__fill_none_items()

    def md_str(self) -> str:
        header_md = f"| {" | ".join(
            self.__replace_pipes(self.headers.md_str_list())
        )} |"
        content_md = "\n".join([
            f"| {" | ".join(self.__replace_pipes(row.md_str_list()))} |"
            for row in self.contents])
        alignment_md = f"| {
            " | ".join([alignment.value for alignment in self.alignments])} |"
        return "\n".join((header_md, alignment_md, content_md))

    def __fill_none_items(self):
        max_columns = max((
            len(self.headers),
            *(len(content) for content in self.contents),
            len(self.alignments)
        ))

        if len(self.headers) < max_columns:
            self.headers.extend(" "*(max_columns - len(self.headers)))
        for row in self.contents:
            if len(row) < max_columns:
                row.extend(" "*(max_columns - len(row)))
        if len(self.alignments) < max_columns:
            self.alignments.extend(
                [Alignment.DEFAULT for _ in range(max_columns - len(self.alignments))])

    def __replace_pipes(self, str_list: list[str]) -> list[str]:
        return [str.replace("|", "&#124;") for str in str_list]

    def __repr__(self) -> str:
        return super().__repr__(headers=self.headers, contents=self.contents, alignments=self.alignments)
