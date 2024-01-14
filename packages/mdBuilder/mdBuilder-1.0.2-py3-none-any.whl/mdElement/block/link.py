from ..element import BlockElement, Text
from ..inline.emphasis import Bold, BoldItalic, Italic
from .image import Image


class Link(BlockElement):
    """The Link element

    `Link(url="mill413.github.io", text_or_image="Link", title="title")` corresponds to `[Link](mill413.github.io "title")` in markdown.

    If there is no given text, it will create an angle brackets enclosed link.

    `Link(url="https://mill413.github.io")` corresponds to `<https://mill413.github.io>` in markdown.

    Notice that the url should start with `https://`, `http://`, `ftp://` or other valid header because some markdown applications won't render it.

    If you want to create a Linking Image, give an Image object to arguments text_or_image.

    `Link(url="mill413.github.io", text_or_image=Image(path_or_url="path/to/image", alt_text="Image", title="image title"))` corresponds to `[![Image](path/to/image "image title")](mill413.github.io)` in markdown.

    Attributes:
        url: a string of url
        text: a string of the link text or the image element's markdown string
        title: a string of the title of link, which is optional
    """

    def __init__(self, url: str, text_or_image: str | Bold | Italic | BoldItalic | Image = "",  title: str = "") -> None:
        super().__init__()
        self.url = url
        self.text = Text(text_or_image) if isinstance(
            text_or_image, str) else text_or_image.md_str()
        self.title = title

    def md_str(self) -> str:
        if self.text == "":
            return f"<{self.url}>"
        else:
            return f"[{self.text.md_str()}]({self.url}{f" \"{self.title}\"" if self.title != "" else ""})"

    def __repr__(self) -> str:
        return super().__repr__(text=self.text, url=self.url, title=self.title)
