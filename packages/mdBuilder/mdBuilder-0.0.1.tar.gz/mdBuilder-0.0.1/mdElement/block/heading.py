from ..element import BlockElement, InlineElement, ElementList


class Heading(BlockElement):
    def __init__(self, level: int, *head: tuple[InlineElement, str]) -> None:
        super().__init__()

        self.head = ElementList(head)
        self.level = level

    def md_str(self) -> str:
        return f"{"#"*self.level} {"".join(self.head.md_str_list())}"

    def __repr__(self) -> str:
        return super().__repr__(head=self.head, level=self.level)
