from ..element import BlockElement

class FrontMatter(BlockElement):
    """a simple Front Matter in YAML"""
    def __init__(self, data: dict) -> None:
        super().__init__()
        self.data = [
            f"{k}: {v}"
            for k, v in data.items()
        ]
    
    def md_str(self) -> str:
        return f"---\n{"\n".join(self.data)}\n---"