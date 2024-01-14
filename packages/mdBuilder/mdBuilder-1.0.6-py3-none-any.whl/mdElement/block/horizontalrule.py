from ..element import BlockElement


class HorizontalRule(BlockElement):
    """The HorizontalRule Element

    `HorizontalRule()` corresponds to `---` in markdown
    """

    def __init__(self) -> None:
        super().__init__()

    def md_str(self) -> str:
        return "---"
