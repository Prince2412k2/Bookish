from typing import List, Optional
from pydantic import BaseModel


class IndustryIdentifier(BaseModel):
    type: str
    identifier: str


class VolumeInfo(BaseModel):
    title: str
    authors: Optional[List[str]] = []
    publisher: Optional[str] = None
    publishedDate: Optional[str] = None
    industryIdentifiers: Optional[List[IndustryIdentifier]] = []


class BookItem(BaseModel):
    kind: str
    id: str  # Google Books unique ID
    volumeInfo: VolumeInfo


class GoogleBooksResponse(BaseModel):
    kind: str
    totalItems: int
    items: Optional[List[BookItem]] = []
