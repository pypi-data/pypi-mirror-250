from pathlib import Path
from typing import Sequence

from mdElement import InlineElement, MdElement, Paragraph


class MdBuilder:
    def __init__(self,
                 *content: tuple[MdElement | str | Sequence[MdElement | str]]) -> None:
        self.content: list[MdElement | str] = []
        for c in content:
            if isinstance(c, Sequence) and not isinstance(c, str):
                for item in c:
                    self.content.append(item)
            else:
                self.content.append(c)

    def write_to_file(self, file: str | Path, mode="w"):
        md_file = file if isinstance(file, Path) else Path(file)

        content_str: str = "\n".join([f"{c.md_str()}\n" if isinstance(c, MdElement)
                                      else c+"\n"
                                     for c in self.content])

        with open(md_file, mode) as f:
            f.write(content_str)
