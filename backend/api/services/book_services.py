import os
from typing import Optional
from fastapi import HTTPException, UploadFile, status
import aiofiles
from qdrant_client import AsyncQdrantClient
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.database.tables import Book
from api.schemas.book_schema import BookSchema
import logging

from module.embeddings import embbed_book

logger = logging.getLogger("uvicorn.error")


async def get_book_by_name(name: str, user_id: int, db: AsyncSession) -> Optional[Book]:
    result = await db.execute(
        select(Book).where(Book.name == name, Book.user_id == user_id)
    )
    return result.scalar_one_or_none()


def strip_file_name(name: str):
    """replace space with underscore for file_management"""
    return os.path.splitext(name.strip())[0].replace(" ", "_")


def file_exist(path: str) -> bool:
    """check if file exists in the path"""
    return os.path.exists(path)


async def validate_epub(file: UploadFile) -> bool:
    """Checks if file has valid epub mime_type"""
    if file.content_type != "application/epub+zip":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type: {file.content_type}. Expected 'application/epub+zip'.",
        )
    return True


def delete_book_file(name: str, user_id: int) -> None:
    """deletes Book to path ./static/<user_id>/<book_name>.epub
    make sure to strip_name
    """
    path = f"./static/{user_id}/{name}.epub"
    if file_exist(path):
        os.remove(path)


async def delete_book_from_db(user_id: int, book_id: int, db: AsyncSession) -> None:
    query = select(Book).where(Book.id == book_id, Book.user_id == user_id)
    result = await db.execute(query)
    book = result.scalar_one_or_none()
    try:
        await db.delete(book)
        await db.commit()
    except IntegrityError:
        logger.exception("Error while deleting")
        raise


async def save_book_file(book_file: UploadFile, user_id: int) -> None:
    """Saves Book to path ./static/<user_id>/<book_name>.epub"""
    assert book_file.filename  # TODO: handle if filename is not present
    name = f"{strip_file_name(book_file.filename)}.epub"

    path = f"./static/{user_id}/"
    os.makedirs(path, exist_ok=True)
    path = os.path.join(path, name)

    if file_exist(path):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="File already exists"
        )
    async with aiofiles.open(f"./static/{user_id}/{name}", "wb") as file:
        await file.write(await book_file.read())


async def add_book_to_db(
    file: UploadFile, user_id: int, db: AsyncSession
) -> BookSchema:
    """saves book_info to database"""
    book_name = file.filename
    assert book_name  # TODO: fix this in future
    book_name = strip_file_name(book_name)
    book_model = BookSchema(user_id=user_id, name=book_name, page=0)
    book = Book(**book_model.model_dump())

    try:
        db.add(book)
        await db.commit()
        await db.refresh(book)
        return book_model
    except IntegrityError:
        await db.rollback()
        delete_book_file(book_name, user_id)
        logger.warning("Book already exists")
        raise
    except Exception:
        await db.rollback()
        delete_book_file(book_name, user_id)
        logger.exception("Error adding book to database")
        raise


async def handle_exceptions(file: UploadFile, user_id, db):
    assert file.filename  # TODO: fix this in future
    await validate_epub(file)
    book_name = strip_file_name(file.filename)
    if await get_book_by_name(book_name, user_id, db):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Book already exists in the database",
        )


async def add_book(
    file: UploadFile, user_id, client: AsyncQdrantClient, db: AsyncSession
) -> BookSchema:
    assert file.filename  # TODO: fix this in future
    await handle_exceptions(file, user_id, db)
    await save_book_file(file, user_id=user_id)
    book = await add_book_to_db(file, user_id, db)
    await embbed_book(book, client)
    return book


async def delete_book(name: str, user_id: int, db: AsyncSession) -> None:
    delete_book_file(strip_file_name(name), user_id)
    book_table = await get_book_by_name(name, user_id, db)
    if book_table:
        await delete_book_from_db(user_id, book_table.id, db)
    return
