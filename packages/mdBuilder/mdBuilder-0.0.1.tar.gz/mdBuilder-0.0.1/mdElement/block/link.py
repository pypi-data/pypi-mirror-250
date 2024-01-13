from ..element import BlockElement, Text
from ..inline.emphasis import Bold, BoldItalic, Italic
from .image import Image


class Link(BlockElement):
    def __init__(self, url: str, text_or_image: str | Bold | Italic | BoldItalic | Image = "",  title: str = "") -> None:
        super().__init__()
        self.url = url
        self.text = Text(text_or_image) if isinstance(
            text_or_image, str) else text_or_image
        self.title = title

    def md_str(self) -> str:
        if self.text == "":
            return f"<{self.url}>"
        else:
            return f"[{self.text.md_str()}]({self.url}{f" \"{self.title}\"" if self.title != "" else ""})"

    def __repr__(self) -> str:
        return super().__repr__(text=self.text, url=self.url, title=self.title)
