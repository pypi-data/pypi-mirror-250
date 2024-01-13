from ..element import BlockElement


class FencedCodeBlock(BlockElement):
    def __init__(self, code: str, syntax: str = "") -> None:
        super().__init__()

        self.syntax = syntax
        self.code = code

    def md_str(self) -> str:
        return f"```{self.syntax}\n{self.code}\n```"

    def __repr__(self) -> str:
        return super().__repr__(syntax=self.syntax, code=self.code)
