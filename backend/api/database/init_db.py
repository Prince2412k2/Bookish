from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from api.database.tables import Base, User, Book

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(bind=engine)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()


async def get_db():
    """get db and close it"""
    async with async_session() as db:
        try:
            yield db
        finally:
            await db.close()
