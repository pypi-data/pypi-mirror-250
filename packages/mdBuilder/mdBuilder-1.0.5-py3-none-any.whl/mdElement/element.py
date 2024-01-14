from abc import ABCMeta, abstractmethod
from collections.abc import Iterable, Iterator
from typing import Self, Sequence


class MdElement(metaclass=ABCMeta):
    """markdown element abstract class"""
    @abstractmethod
    def md_str(self) -> str:
        """return element's markdown string

        Implemented by children class.

        Return:
            a string, which is a markdown string of this element.
        """
        pass

    def __repr__(self, show_more=False, **info: dict) -> str:
        base_info: dict = {
            "name": self.__class__.__name__,
            "markdown": self.md_str()
        }
        if show_more:
            base_info.update(info)
        return str(base_info)


class InlineElement(MdElement, metaclass=ABCMeta):
    """inline element abstract class

    The element which can be nested in text.

    Include elements of Code, Emphasis(Bold, Italic, BoldItalic), Strikethrough.

    Attributes:
        content: simple text string
        symbol: the symbol of this element, such as *, **, ~~ etc.
    """

    def __init__(self, content: str, symbol: str) -> None:
        """init InlineElement with content and symbol"""
        super().__init__()
        self.content = content
        self.symbol = symbol

    def md_str(self) -> str:
        return f"{self.symbol}{self.content}{self.symbol}"


class BlockElement(MdElement, metaclass=ABCMeta):
    """block element abstract class

    The element which may have many lines and other elements.

    Include elements of Heading, Table etc.
    """

    def __init__(self) -> None:
        """init BlockElement with content"""
        super().__init__()

    @abstractmethod
    def md_str(self) -> str:
        pass


class Text(MdElement):
    """str wrapper

    Wrap string to a markdown element.

    Attributes:
        text: a string of text
    """

    def __init__(self, text: str) -> None:
        """init Text with text"""
        super().__init__()
        self.text = text

    def md_str(self) -> str:
        return self.text


class ElementList(list):
    """a list of MdElement

    Aiming to handle list of elements, which can be nested in another ElementList

    Attributes:
        elements: a list including MdElement and other ElementList
    """

    def __init__(self, elements: Sequence[MdElement | str | Self]) -> None:
        """init elements with a sequence of MdElements or string or other ElementLists

        The string element will be wrapped to Text
        """
        self.elements: list[MdElement | Self] = [
            Text(e) if isinstance(e, str) else e
            for e in elements]

    def md_str_list(self) -> list[str | list]:
        """get a list of elements' markdown string

        Returns:
            a list of the elements' markdown string, such as:

            ["Element", "**Bold**"]

            If the element is a ElementList, the md_str_list will be added in.
        """
        return [
            e.md_str() if isinstance(e, MdElement) else e.md_str_list()
            for e in self.elements]

    def __repr__(self) -> str:
        return self.__class__.__name__+str([e.__repr__() for e in self.elements])

    def __len__(self) -> int:
        return len(self.elements)

    def extend(self, __iterable: Iterable) -> None:
        iterable = [Text(str(item)) if not isinstance(
            item, MdElement) else item for item in __iterable]
        return self.elements.extend(iterable)

    def __iter__(self) -> Iterator:
        return self.elements.__iter__()
