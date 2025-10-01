from typing import Any, Dict, List, Optional
from pathlib import Path
import logging
from pydantic import BaseModel, Field
from zipfile import ZipFile
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
import warnings
from uuid import UUID, uuid4

from book_parser.base import Epub

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)


##file imports

logger = logging.getLogger(__name__)


def validate_epub(path: Path) -> Optional[bool]:
    """returns a Epub obj given a valid path"""
    if not path.exists():
        raise ValueError("File doesnt exist")
    ext = path.suffix
    if ext == ".epub":
        try:
            return True
        except Exception as e:
            logger.error(f"Possibly corrupted file : {e}")
    else:
        raise ValueError("Only epub is supported for now")


def get_book(book_path: Path) -> Optional[Epub]:
    return Epub(book_path).initialize()


def set_chapter(
    id: int,
    chapter_name: str,
    content: str,
) -> "Chapter":
    return Chapter(
        chapter_id=str(id), title=chapter_name, content=content.replace(r"\n", "\n")
    )


def get_html_files(path: Path):
    html: Dict[str, str] = {}
    with ZipFile(path) as file:
        for i in file.namelist():
            if Path(i).suffix in (".html", ".xhtml"):
                with file.open(i) as chapter:
                    soup = BeautifulSoup(chapter.read().decode("utf-8"), "lxml")
                    content = soup.body
                    if not content:
                        content = soup
                    html[i] = content.get_text(separator=r"\n", strip=True)

    return html


def set_chapters(book: "Book") -> None:
    assert book.file
    html_files = get_html_files(book.path)
    try:
        book.chapters = [
            set_chapter(id=idx + 1, chapter_name=k, content=v)
            for idx, (k, v) in enumerate(html_files.items())
        ]
    except Exception as e:
        raise Exception(e)


def set_metadata(book: "Book"):
    assert book.file
    book.metadata = book.file.get_meta()


def set_title(book: "Book"):
    for k, v in book.metadata.items():
        if k.lower().strip() == "title":
            book.name = v
            return


class Chapter(BaseModel):
    """Stores a chapter"""

    chapter_id: str
    title: str
    content: str

    def __repr__(self) -> str:
        return f"{self.chapter_id}"


class Book(BaseModel):
    """use book.load(path:str) where book is instance of Book"""

    model_config = {"arbitrary_types_allowed": True}
    path: Path = Field(default=Path(""), exclude=True)
    name: str = Field(default="", exclude=True)
    id: str = Field(default="", exclude=True)
    file: Optional[Epub] = None
    chapters: List[Chapter] = Field(default_factory=list, exclude=True)
    metadata: Dict[Any, Any] = Field(default_factory=dict, exclude=True)

    def load(self, path_to_book: str):
        path = Path(path_to_book)
        self.name = path.stem
        self.path = path if validate_epub(path) else Path("")
        self.file = get_book(self.path)
        self.id = str(uuid4())
        set_chapters(self)
        set_metadata(self)
        set_title(self)

    def get_all_chap(self):
        return "".join([i.content for i in self.chapters])

    def get_meta(self):
        return self.metadata


def test_1():
    book = Book()
    book.load(
        path_to_book="/home/prince/projects/Bookish/backend/module/book_parser/SeaStories.epub"
    )
    return book


def test():
    path = Path("/home/prince/projects/book2/tests/stuff/test_books/AF.epub")
    with ZipFile(path) as file:
        for i in file.namelist():
            if Path(i).suffix in (".html", ".xhtml"):
                with file.open(i) as chapter:
                    soup = BeautifulSoup(chapter.read().decode("utf-8"), features="xml")

                print(soup.get_text(separator="\n", strip=True))
