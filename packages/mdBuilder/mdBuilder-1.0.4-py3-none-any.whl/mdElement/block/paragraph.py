from ..element import BlockElement, ElementList, InlineElement


class Paragraph(BlockElement):
    """The Paragraph Element

    `Paragraph("Text1", Bold("Text2"))` corresponds to `Text1**Text2**` in markdown
    """

    def __init__(self, *content: tuple[InlineElement | str]) -> None:
        super().__init__()

        self.content = [c for c in content]

    def md_str(self) -> str:
        return "".join(c.md_str() if isinstance(c, InlineElement) else c for c in self.content)
