from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from api.database.init_db import get_db
from api.database.tables import User
from api.services.auth import (
    authenticate_user,
    create_access_token,
)
from api.schemas.login_schema import Token, UserResponseSchema, UserSchema

from fastapi import APIRouter, Depends, HTTPException, status

from api.services.user_services import add_user

login_router = APIRouter()


@login_router.post("/login/", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(form_data.username, form_data.password, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = create_access_token(data={"sub": str(user.id)})
    return access_token


@login_router.post("/register", response_model=UserResponseSchema)
async def register_user(user: UserSchema, db: AsyncSession = Depends(get_db)):
    db_user = await add_user(user, db)
    return UserResponseSchema.model_validate(db_user)
