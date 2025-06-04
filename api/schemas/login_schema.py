from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional


from enum import StrEnum


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TypeUser(StrEnum):
    FREE = "FREE"
    PAID = "PAID"


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
