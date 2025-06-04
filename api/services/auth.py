from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from api.database.init_db import get_db


from typing import Annotated, Awaitable, Optional, Union
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import timedelta, datetime, timezone

from api.database.tables import User

app = FastAPI()

SECRET_KEY = "12nfj45647dghs74e7du4e89i4er98ie984we98i4w094oew"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return bcrypt_context.hash(password)


def verify_hash(password: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(secret=password, hash=hashed_password)


def create_acess_token(
    data: dict, expiration_time: timedelta = timedelta(minutes=15)
) -> Optional[str]:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expiration_time
    to_encode["exp"] = expire
    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except JWTError:
        raise


async def authenticate_user(username: str, password: str, db: AsyncSession) -> User:
    stmt = select(User).where(User.name == username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if user and verify_hash(password, user.password):
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrrect Credentials",
        )
