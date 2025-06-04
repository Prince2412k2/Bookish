from typing import List, Optional
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs

from api.schemas.models import TypeUser

# TODO: add type of users e.g. paid/unpaid.
# TODO: add credit system for usage data.


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    user_type: Mapped[str] = mapped_column(nullable=False)
    current_book_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("books.id"), nullable=True
    )

    current_book: Mapped[Optional["Book"]] = relationship(
        foreign_keys=[current_book_id], uselist=False
    )

    books: Mapped[List["Book"]] = relationship(
        back_populates="user", foreign_keys="[Book.user_id]"
    )

    def __repr__(self) -> str:
        return f"<User:{self.name} has {len(self.books)} books and currently reading {self.current_book_id}>"


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    page: Mapped[int]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped[User] = relationship(back_populates="books", foreign_keys=[user_id])

    def __repr__(self) -> str:
        return f"<Book:{self.name} with id:{self.id}>"
