from ..element import BlockElement


class FencedCodeBlock(BlockElement):
    """The Fenced Code Block element
    
    `FencedCodeBlock("print("Code")", syntax="python")` corresponds to
    
    ```````
    ```python
    print("Code")
    ```
    ```````

    in markdown

    Attributes:
        syntax: a string of syntax name
        code: the content in code block
    """
    def __init__(self, code: str, syntax: str = "") -> None:
        super().__init__()

        self.syntax = syntax
        self.code = code

    def md_str(self) -> str:
        return f"```{self.syntax}\n{self.code}\n```"

    def __repr__(self) -> str:
        return super().__repr__(syntax=self.syntax, code=self.code)
