from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from utils.logger_module import configure_logger
from api.database.schema import UserSchema, BookSchema
from api.database.models import User, Book
from api.database.init_db import init_db, get_db

logger = configure_logger(log_level=logging.INFO)

app = FastAPI()


@app.post("/users")
async def create_user(user: UserSchema, db: AsyncSession = Depends(get_db)):
    new_user = User(**user.dict())  # Unpack Pydantic fields
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user  # Or use a Pydantic response model if you prefer
