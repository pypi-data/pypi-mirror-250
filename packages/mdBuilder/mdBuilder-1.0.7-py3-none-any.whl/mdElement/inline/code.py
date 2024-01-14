from ..element import InlineElement


class Code(InlineElement):
    """The Code Element

    `Code("Text")` corresponds to ``` `Text` ``` in markdown
    """

    def __init__(self, content: str) -> None:
        super().__init__(content, symbol="`")  # TODO-handle ` in content
