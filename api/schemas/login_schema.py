from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

from api.schemas.models import TypeUser


class Token(BaseModel):
    access_token: str
    token_type: str


class UserSchema(BaseModel):
    name: str
    password: str
    email: EmailStr
    current_book_id: Optional[int] = None
    user_type: TypeUser

    class Config:
        from_attributes = True


class UserResponseSchema(BaseModel):
    name: str
    email: EmailStr
    current_book_id: Optional[int] = None
    user_type: TypeUser

    class Config:
        from_attributes = True
