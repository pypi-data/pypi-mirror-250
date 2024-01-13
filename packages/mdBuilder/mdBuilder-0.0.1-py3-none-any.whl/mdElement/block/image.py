from pathlib import Path

from ..element import BlockElement


class Image(BlockElement):
    def __init__(self, path_or_url: str | Path, alt_text: str = "", title: str = "") -> None:
        super().__init__()

        self.image = path_or_url  # TODO - handle string file path
        self.text = alt_text
        self.title = title

    def md_str(self) -> str:
        return f"![{self.text}]({self.image}{f" \"{self.title}\"" if self.title != "" else ""})"

    def __repr__(self) -> str:
        return super().__repr__(
            image=self.image if isinstance(
                self.image, str) else self.image.absolute,
            alt_text=self.text,
            title=self.title)
