from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from api.database.init_db import get_db
from api.database.tables import User
from api.services.auth import (
    authenticate_user,
    create_acess_token,
)
from api.schemas.login_schema import Token, UserResponseSchema, UserSchema

from fastapi import APIRouter, Depends, HTTPException

from api.services.user_services import add_user

login_router = APIRouter()


@login_router.post("/login/")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(form_data.username, form_data.password, db=db)
    return create_acess_token(data={"sub": user.id})


@login_router.post("/register")
async def register_user(user: UserSchema, db: AsyncSession = Depends(get_db)):
    db_user = await add_user(user, db)
    return UserResponseSchema.model_validate(db_user)
