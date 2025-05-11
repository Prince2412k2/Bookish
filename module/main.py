from typing import List
from book_parser.main import Book
import subprocess
from pydantic import BaseModel


class WordInstance(BaseModel):
    safe: List[str]
    spoiler: List[str]
    sentence: str
    word: str


def get_instance_of_word(word: str, content: str) -> list:
    pattern = rf"\b{word}([-a-z]*)?\b"
    result = subprocess.run(
        ["grep", "-i", "-E", "-A", "2", "-B", "2", pattern],
        input=content,
        text=True,
        capture_output=True,
    )
    return result.stdout.split("--")


def split_book(book: Book, sentance: str):
    return book.get_all_chap().split(sentance)


def get_instances(book: Book, sentance: str, word: str):
    sentance = sentance.lower()
    safe, spoiler = split_book(book, sentance)
    return WordInstance(
        safe=get_instance_of_word(content=safe, word=word)[-5:],
        spoiler=get_instance_of_word(content=spoiler, word=word)[:5],
        word=word,
        sentence=sentance,
    )


def main() -> None:
    path = "/home/prince/projects/book2/tests/stuff/test_books/LP.epub"
    book = Book()
    book.load(path_to_book=path)
    sentence = """never wished you any sort of harm; but you wanted me to tame you ."""


if __name__ == "__main__":
    main()
