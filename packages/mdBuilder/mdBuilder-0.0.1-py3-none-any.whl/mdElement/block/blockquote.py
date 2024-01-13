from ..element import MdElement, BlockElement, ElementList


class Blockquote(BlockElement):
    def __init__(self, *quote: tuple[MdElement, str]) -> None:
        super().__init__()

        self.content = ElementList(quote)

    def md_str(self) -> str:
        quote_list = []
        for ind, block in enumerate(self.content.md_str_list()):
            quote_list.append(block)
            if ind != (len(self.content.elements)-1):
                quote_list.append("")

        return "\n".join([f"> {p}".strip() for p in list(quote_list)])

    def __repr__(self) -> str:
        return super().__repr__(content=self.content)
