from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio


async def test_db():
    engine = create_async_engine(
        "postgresql+asyncpg://postgres@localhost:5432/postgres"
    )

    async with engine.connect() as conn:
        session = AsyncSession(conn)
        session.execute(a)
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(test_db())
