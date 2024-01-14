from ..element import BlockElement


class Image(BlockElement):
    """The Image Element

    `Image(path_or_url="path/to/image", alt_text="Image", title="title")` corresponds to `![Image](path/to/image "title")` in markdown

    Attributes:
        text: a string of alt text
        image: a string of the image's url or local path
        title: a string of the title of this image, which is optional
    """

    def __init__(self, path_or_url: str, alt_text: str = "", title: str = "") -> None:
        super().__init__()

        self.text = alt_text
        self.image = path_or_url
        self.title = title

    def md_str(self) -> str:
        return f"![{self.text}]({self.image}{f" \"{self.title}\"" if self.title != "" else ""})"

    def __repr__(self) -> str:
        return super().__repr__(
            image=self.image if isinstance(
                self.image, str) else self.image.absolute,
            alt_text=self.text,
            title=self.title)
