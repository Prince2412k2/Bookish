from pathlib import Path
import unittest

from book_parser.main import validate_epub, get_book
from book_parser.base import Epub


class TestEpubValidation(unittest.TestCase):
    def test_validate_epub_unsupporeted(self):
        path = "./tests/stuff/test_books/LP.pdf"
        with self.assertRaises(ValueError):
            validate_epub(Path(path))

    def test_validate_epub_bad_path(self):
        path = "./tests/stuff/test_books/KB.pdf"
        with self.assertRaises(ValueError):
            validate_epub(Path(path))

    def test_validate_epub_good(self):
        path = "./tests/stuff/test_books/LP.epub"
        self.assertEqual(validate_epub(Path(path)), True)


class TestEpubGetBook(unittest.TestCase):
    def test_get_book_valid(self):
        path = "./tests/stuff/test_books/LP.epub"
        self.assertIsInstance(get_book(Path(path)), Epub)

    def test_get_book_invalid(self):
        path = "./tests/stuff/test_books/LP.pdf"
        with self.assertRaises(ValueError):
            get_book(Path(path))
