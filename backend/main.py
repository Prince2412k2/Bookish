import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager

from api.database.init_db import create_db
from api.endpoints.user_route import login_router
from api.endpoints.book_route import book_router
import uvicorn

logger = logging.getLogger("uvicorn.error")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("starting up the app")
    await create_db()
    logger.info("create_db")
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(login_router, prefix="/user")
app.include_router(book_router, prefix="/book")


@app.get("/")
async def helo():
    return {"helo": "world"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, reload=True)
