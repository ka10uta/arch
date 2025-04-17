import asyncio
from time import sleep
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import StreamingResponse

import logging
import uvicorn

logging.basicConfig(
    level=logging.INFO,
    format=(
        '{'
        '"time": "%(asctime)s", '
        '"level": "%(levelname)s", '
        '"message": "%(message)s"'
        '}'
    ),
    datefmt="%Y-%m-%dT%H:%M:%S%z",
)

app = FastAPI()

logger = logging.getLogger(__name__)

class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            logger.info(f"TimingMiddleware: {request.url}")
            response = await call_next(request)
            logger.info(f"TimingMiddleware: {response}")
            return response
        finally:
            logger.info("TimingMiddleware")

app.add_middleware(TimingMiddleware)

def slow_numbers(limit: int):
    for i in range(limit):
        if i == 0:
            logger.info("sleep 5")
            sleep(5)
        elif i == 4:
            raise Exception("error")
        else:
            logger.info("sleep 1")
            sleep(1)
        yield f"data: {i}\n\n"

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/stream")
def stream_response():
    sleep(3)
    logger.info("stream_response")
    return StreamingResponse(
        slow_numbers(5),
        media_type="text/event-stream"
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
