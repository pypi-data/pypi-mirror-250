from ..element import BlockElement, InlineElement, ElementList


class Paragraph(BlockElement):
    def __init__(self, *content: tuple[InlineElement, str]) -> None:
        super().__init__()

        self.content = ElementList(content)

    def md_str(self) -> str:
        return "".join(self.content.md_str_list()).strip()
