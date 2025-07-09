from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class BookSchema(BaseModel):
    name: str
    user_id: int
    page: int

    class Config:
        from_attributes = True
