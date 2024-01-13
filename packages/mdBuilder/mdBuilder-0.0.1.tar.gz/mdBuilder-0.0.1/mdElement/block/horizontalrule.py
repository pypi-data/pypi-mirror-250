from ..element import BlockElement


class HorizontalRule(BlockElement):
    def __init__(self) -> None:
        super().__init__()

    def md_str(self) -> str:
        return "---"
