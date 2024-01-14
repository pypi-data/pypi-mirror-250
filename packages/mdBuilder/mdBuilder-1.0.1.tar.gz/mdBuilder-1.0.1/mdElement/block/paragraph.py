from ..element import BlockElement, ElementList, InlineElement


class Paragraph(BlockElement):
    """The Paragraph Element

    `Paragraph("Text1", "Text2")` corresponds to 

    ```markdown
    Text1

    Text2
    ```
    in markdown
    """

    def __init__(self, *content: tuple[InlineElement, str]) -> None:
        super().__init__()

        self.content = ElementList(content)

    def md_str(self) -> str:
        return "".join(self.content.md_str_list()).strip()
