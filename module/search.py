from typing import List
from book_parser.main import Book
import subprocess
from pydantic import BaseModel
import re


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


def normalize_whitespace(text: str) -> str:
    # Collapse all whitespace (spaces, tabs, newlines) into a single space
    return re.sub(r"\s+", " ", text).strip()


def split_text(content: str, sentance: str):
    sentance = normalize_whitespace(sentance)
    content = normalize_whitespace(content)
    if sentance not in content:
        raise ValueError("sentence not in book")
    return content.split(sentance)


def get_word_obj(book: Book, sentance: str, word: str):
    instances = get_instance_of_word(content=book.get_all_chap(), word=word)
    context = instances[:5] + instances[-5:] if len(instances) > 10 else instances
    return WordInstance(
        context=context,
        word=word,
        sentence=sentance,
    )


# def get_selection_chp(book: Book, selection: str):
#     for idx, i in enumerate(book.chapters):
#         if selection in i.content:
#             chapter = i.content
#             before = book.chapters[idx - 1].content if idx > 1 else ""
#             after = book.chapters[idx + 1].content if idx < len(book.chapters) else ""
#             return f"{before[-len(chapter) :]}{chapter}{after[: len(chapter)]}"
#         else:
#             raise ValueError(f"Could not find given selection:  {selection}")
#


def get_selection_obj(
    book: Book,
    selection: str,
):
    sections = split_text(book.get_all_chap(), selection)
    if len(sections) != 2:
        raise ValueError(f"invalid valaue {len(sections)}")
    safe, spoiler = sections
    return SelectionInstance(
        safe_context="...." + safe[-2000:],
        spoiler_context=spoiler[:2000] + "....",
        selection=selection,
    )


def main() -> None:
    path = "/home/prince/projects/book2/tests/stuff/test_books/LP.epub"
    book = Book()
    book.load(path_to_book=path)
    sentence = """she echoed. "I think there
are six or seven of them in existence. I saw them, several years
ago. But one never knows where to find them. The wind blows them"""
    # print(get_selection_obj(book, sentence).model_dump_json())
    print(book.get_all_chap())


if __name__ == "__main__":
    main()
