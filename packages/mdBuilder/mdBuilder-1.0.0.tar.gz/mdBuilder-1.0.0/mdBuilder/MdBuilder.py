from mdElement import MdElement, InlineElement, Paragraph
from pathlib import Path


class MdBuilder:
    def __init__(self,
                 *content: tuple[MdElement | str]) -> None:
        self.content: list[MdElement | str] = [
            Paragraph(c) if isinstance(c, InlineElement)
            else c for c in content]

    def write_to_file(self, file: str | Path, mode="w"):
        md_file = file if isinstance(file, Path) else Path(file)

        content_str: str = "\n".join([f"{block.md_str()}\n" if isinstance(block, MdElement)
                                      else block+"\n"
                                     for block in self.content])

        with open(md_file, mode) as f:
            f.write(content_str)
