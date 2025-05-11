from typing import List
from book_parser.main import Book
import subprocess
from pydantic import BaseModel


class WordInstance(BaseModel):
    context: List[str]
    sentence: str
    word: str


class SelectionInstance(BaseModel):
    safe_context: str
    spoiler_context: str
    selection: str


def get_instance_of_word(word: str, content: str) -> list:
    pattern = rf"\b{word}([-a-z]*)?\b"
    result = subprocess.run(
        ["grep", "-i", "-E", "-A", "2", "-B", "2", pattern],
        input=content,
        text=True,
        capture_output=True,
    )
    return result.stdout.split("--")


def split_text(content: str, sentance: str):
    return content.split(sentance)


def get_word_obj(book: Book, sentance: str, word: str):
    sentance = sentance.lower()
    instances = get_instance_of_word(content=book.get_all_chap(), word=word)
    context = instances[:5] + instances[-5:] if len(instances) > 10 else instances
    return WordInstance(
        context=context,
        word=word,
        sentence=sentance,
    )


def get_selection_chp(book: Book, selection: str):
    for idx, i in enumerate(book.chapters):
        if selection in i.content:
            chapter = i.content
            before = book.chapters[idx - 1].content if idx > 1 else ""
            after = book.chapters[idx + 1].content if idx < len(book.chapters) else ""
            return f"{before[-len(chapter) :]}{chapter}{after[: len(chapter)]}"
        else:
            raise ValueError(f"Could not find given selection {selection}")


def get_selection_obj(
    book: Book,
    selection: str,
):
    chapter = get_selection_chp(book, selection)
    assert chapter
    safe, spoiler = split_text(chapter, selection)
    return SelectionInstance(
        safe_context=safe, spoiler_context=spoiler, selection=selection
    )


def main() -> None:
    path = "/home/prince/projects/book2/tests/stuff/test_books/LP.epub"
    book = Book()
    book.load(path_to_book=path)
    sentence = """never wished you any sort of harm; but you wanted me to tame you ."""


if __name__ == "__main__":
    main()
