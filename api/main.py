from fastapi import FastAPI
import uvicorn
import logging
from utils.logger_module import configure_logger

logger = configure_logger(log_level=logging.INFO)

app = FastAPI()


@app.get("/")
def helloword():
    return {"helo": "world"}


def main():
    uvicorn.run("api.main:app", log_level="info")
