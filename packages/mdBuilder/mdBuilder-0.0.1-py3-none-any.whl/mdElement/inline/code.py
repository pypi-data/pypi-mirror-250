from ..element import InlineElement


class Code(InlineElement):
    def __init__(self, content: str) -> None:
        super().__init__(content, symbol="`")
