from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from api.database.models import Base, User, Book
from contextlib import asynccontextmanager

DATABASE_URL = "postgresql+asyncpg://postgres@localhost:5432/postgres"
# DATABASE_URL = "sqlite+aiosqlite:///"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(bind=engine)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()


@asynccontextmanager
async def get_db():
    """get db and close it"""
    db = async_session()
    try:
        yield db
    finally:
        await db.close()
