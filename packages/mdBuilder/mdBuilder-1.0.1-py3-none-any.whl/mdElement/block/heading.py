from ..element import BlockElement, ElementList, InlineElement


class Heading(BlockElement):
    """The Heading Element

    `Heading(1, "Heading")` corresponds to `# Heading` in markdown

    Attributes:
        level: a integer of the heading's level, which corresponds to the number of sighs(#) in front of the text
        text: a string of a word or phrase
    """

    def __init__(self, level: int, *head: tuple[InlineElement, str]) -> None:
        super().__init__()

        self.level = level
        self.head = ElementList(head)

    def md_str(self) -> str:
        return f"{"#"*self.level} {"".join(self.head.md_str_list())}"

    def __repr__(self) -> str:
        return super().__repr__(head=self.head, level=self.level)
