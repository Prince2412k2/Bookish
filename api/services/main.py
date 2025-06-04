from sqlalchemy.ext.asyncio import AsyncSession
from api.database.tables import Base, User, Book
from api.models.models import UserSchema, BookSchema


# TODO: add password hashing
async def register_user(user: UserSchema, db: AsyncSession):
    new_user = User(user)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user.id
