from sqlalchemy import insert, select
from api.database.init_db import create_db, get_db
import asyncio

from api.database.models import User


async def make():
    await create_db()
    async with get_db() as db:
        user = User(name="prince")
        result = db.add(user)
        await db.commit()
        await db.refresh(user)


asyncio.run(make())
