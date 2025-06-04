from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from enum import StrEnum


class TypeUser(StrEnum):
    FREE = "FREE"
    PAID = "PAID"


class BookSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    user_id: str
    page: int
