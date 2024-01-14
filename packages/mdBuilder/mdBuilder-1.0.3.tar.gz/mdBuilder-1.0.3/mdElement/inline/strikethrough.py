from ..element import InlineElement


class Strikethrough(InlineElement):
    """The Strikethrough Element

    `Strikethrough("Text")` corresponds to `~~Text~~` in markdown
    """

    def __init__(self, content: str) -> None:
        super().__init__(content, symbol="~~")
