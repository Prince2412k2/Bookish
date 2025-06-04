from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from api.database.tables import User
from api.schemas.login_schema import UserSchema
from logging import getLogger

from api.services.auth import hash_password

logger = getLogger("uvicorn.error")


async def get_user(id: int, db: AsyncSession) -> User:
    """get user from db with id:int"""
    query = select(User).where(User.id == id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail=f"user with {id=} not found")
    return user


async def add_user(user: UserSchema, db: AsyncSession) -> User:
    """add user to database"""
    user.password = hash_password(user.password)
    user_table = User(**user.model_dump(mode="python"))
    try:
        db.add(user_table)
        await db.commit()
        await db.refresh(user_table)
        return user_table

    except IntegrityError as e:
        logger.warning(f"[add_user] : {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )
    except Exception as e:
        logger.warning(f"[add_user] : {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
