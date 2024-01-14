from ..element import InlineElement


class Italic(InlineElement):
    """The Italic Element

    `Italic("Text")` corresponds to `*Text*` in markdown
    """

    def __init__(self, content: str) -> None:
        super().__init__(content, symbol="*")


class Bold(InlineElement):
    """The Bold Element

    `Bold("Text")` corresponds to `**Text**` in markdown
    """

    def __init__(self, content: str) -> None:
        super().__init__(content, symbol="**")


class BoldItalic(InlineElement):
    """The BoldItalic Element

    `BoldItalic("Text")` corresponds to `***Text***` in markdown
    """

    def __init__(self, content: str) -> None:
        super().__init__(content, symbol="***")
