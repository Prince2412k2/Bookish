from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID


class BookSchema(BaseModel):
    name: str
    user_id: str
    page: int

    class Config:
        from_attributes = True


class UserSchema(BaseModel):
    name: str
    books: List[BookSchema]
    current_book_id: Optional[UUID]

    class Config:
        from_attributes = True
