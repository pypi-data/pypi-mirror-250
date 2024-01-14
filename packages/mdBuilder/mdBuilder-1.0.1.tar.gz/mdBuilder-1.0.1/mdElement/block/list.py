from abc import ABCMeta, abstractmethod
from typing import Self

from ..element import BlockElement, Text
from .blockquote import Blockquote
from .image import Image
from .paragraph import Paragraph

ListItem = Text | Paragraph | Blockquote | Image | Self


class List(BlockElement, metaclass=ABCMeta):
    """The List element

    Attributes:
        items: a list of the items of the List
    """

    def __init__(self, *items: tuple[str | list[str | Paragraph | Blockquote | Image | Self]]) -> None:
        super().__init__()
        self.items: list[list[ListItem]] = [
            [Text(item)] if isinstance(item, str)
            else [Text(i) if isinstance(i, str)
                  else i
                  for i in item]
            for item in items
        ]
        for item in self.items:
            self._check_list_(item)

    def md_str(self, bias: str = "") -> str:
        return self._to_md_str_(bias)

    def __repr__(self) -> str:
        return super().__repr__(items=self.items)

    def _check_list_(self, item_list: list[ListItem]) -> bool:
        for ind, item in enumerate(item_list):
            if ind == 0:
                assert isinstance(
                    item, Text), "First element in a list item should be str"
            else:
                assert isinstance(
                    item, (Text, Paragraph, Blockquote, Image, List)), "The element must be paragraph, blockquote, image or list"

    @abstractmethod
    def _to_md_str_(self, bias: str = "") -> str:
        ...


class OrderedList(List):
    """The Ordered List element

    Attributes:
        items: a list of the items of the Ordered List
        start: the start index.Recommend for default 1
    """

    def __init__(self, *items: tuple[str | list[str | Paragraph | Blockquote | Image | List]], start_index: int = 1) -> None:
        super().__init__(*items)
        self.start: int = start_index

    def _to_md_str_(self, bias: str = "") -> str:
        md_str_list = []
        for item_ind, item_list in enumerate(self.items):
            if len(item_list) == 1:
                md_str_list.append(
                    f"{bias}{self.start + item_ind}. "+item_list[0].md_str())
            else:
                for ind, item in enumerate(item_list):
                    item_str_list = [
                        f"{bias}{self.start + item_ind}. "+item.md_str() if ind == 0
                        else
                        f"\n{bias}    "+item.md_str() if isinstance(item, (Text, Paragraph, Blockquote, Image))
                        else f"\n{item.md_str(bias=bias+"    ")}"
                    ]
                    md_str_list.append("\n".join(item_str_list))

        return "\n".join(md_str_list)


class UnorderedList(List):
    """The Unordered List element

    Attributes:
        items: a list of the items of the Unordered List
    """

    def _to_md_str_(self, bias: str = "") -> str:
        md_str_list = []
        for _, item_list in enumerate(self.items):
            if len(item_list) == 1:
                md_str_list.append(f"{bias}* "+item_list[0].md_str())
            else:
                for ind, item in enumerate(item_list):
                    item_str_list = [
                        f"{bias}* "+item.md_str() if ind == 0
                        else
                        f"\n{bias}    "+item.md_str() if isinstance(item, (Text, Paragraph, Blockquote, Image))
                        else f"\n{item.md_str(bias=bias+"    " if isinstance(item, OrderedList) else "  ")}"
                    ]
                    md_str_list.append("\n".join(item_str_list))

        return "\n".join(md_str_list)


class TaskList(List):
    ...
