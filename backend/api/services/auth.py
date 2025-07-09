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
from api.schemas.login_schema import Token

from dotenv import load_dotenv
import os

load_dotenv()


try:
    SECRET_KEY = os.environ["SECRET_KEY"]
    ALGORITHM = os.environ["ALGORITHM"]
except KeyError as e:
    raise RuntimeError(f"Missing required environment variable: {e.args[0]}")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return bcrypt_context.hash(password)


def verify_hash(password: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(secret=password, hash=hashed_password)


def create_access_token(
    data: dict, expiration_time: timedelta = timedelta(minutes=15)
) -> Token:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expiration_time
    to_encode.update({"exp": expire})

    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return Token(access_token=encoded_jwt)
    except JWTError as e:
        # Optional: log or handle specific errors
        raise ValueError(f"Token encoding failed: {str(e)}")


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


def get_current_user(token: str = Depends(oauth2_scheme)) -> int:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="invalid toekn")
        return int(user_id)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or malformed token")
