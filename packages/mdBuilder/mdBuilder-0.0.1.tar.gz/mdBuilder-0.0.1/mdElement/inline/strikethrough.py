from ..element import InlineElement


class Strikethrough(InlineElement):
    def __init__(self, content: str) -> None:
        super().__init__(content, symbol="~~")
