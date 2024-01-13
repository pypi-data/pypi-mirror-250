from ..element import InlineElement


class Bold(InlineElement):
    def __init__(self, content: str) -> None:
        super().__init__(content, symbol="**")


class Italic(InlineElement):
    def __init__(self, content: str) -> None:
        super().__init__(content, symbol="*")


class BoldItalic(InlineElement):
    def __init__(self, content: str) -> None:
        super().__init__(content, symbol="***")
