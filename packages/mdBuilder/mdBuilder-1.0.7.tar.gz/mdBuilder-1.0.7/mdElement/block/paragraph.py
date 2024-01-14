from ..element import BlockElement, InlineElement
from .link import Link


class Paragraph(BlockElement):
    """The Paragraph Element

    `Paragraph("Text1", Bold("Text2"))` corresponds to `Text1**Text2**` in markdown
    """

    def __init__(self, *content: tuple[InlineElement | str | Link]) -> None:
        super().__init__()

        self.content = [c for c in content]

    def md_str(self) -> str:
        return "".join(c.md_str() if not isinstance(c, str) else c for c in self.content)
