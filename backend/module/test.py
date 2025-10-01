from book_parser.main import Book, test_1
from rag.qdrant import embbed_book, search
import asyncio


async def run():
    book = test_1()
    await embbed_book(book)
    output = await search(book.id, "what")
    print(output)


asyncio.run(run())
