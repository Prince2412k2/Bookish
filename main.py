from api.database.init_db import get_db, init_db
from api.database.models import Book, User
from api.database.schema import BookSchema, UserSchema
import asyncio


async def create_book(book: BookSchema):
    async for db in get_db():
        new_book = Book(**book.model_dump())
        db.add(new_book)
        await db.commit()
        await db.refresh(new_book)
        return new_book


async def test():
    await init_db()
    await create_book(BookSchema(name="LP", user_id="wdefrgt", page=20))


if __name__ == "__main__":
    asyncio.run(test())
