from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from api.database.init_db import get_db
from api.schemas.book_schema import BookSchema
from api.services.auth import get_current_user
import logging

from api.services.book_services import add_book, delete_book

logger = logging.getLogger("uvicorn.errors")

book_router = APIRouter()


@book_router.post("/upload", response_model=BookSchema)
async def save_book(
    file: UploadFile,
    user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await add_book(file, user_id, db)


@book_router.post("/delete")
async def remove_book(
    book_name: str,
    user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await delete_book(book_name, user_id, db)
