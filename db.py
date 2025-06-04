from sqlalchemy import insert, select
from api.database.init_db import create_db, get_db
import asyncio

from api.services.main import register_user
from api.database.tables import User
from api.models.models import UserSchema


async def make():
    await create_db()
    user = UserSchema(
        name="Prince",
        password="qwertyu",
        email="Prince2412001@gmail.com",
    )
    async with get_db() as db:
        await register_user(user, db=db)


asyncio.run(make())
