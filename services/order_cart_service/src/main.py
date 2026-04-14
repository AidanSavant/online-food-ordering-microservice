import os
import logging
from contextlib import asynccontextmanager

from errors.exceptions import CartBaseException
from handlers.cart import get_repository, router
from repository.impls.redis import RedisCartRepository

import redis.asyncio as redis

from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.responses import JSONResponse

load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting order cart service...")

    redis_url = os.getenv("REDIS_URL")
    if redis_url is None:
        raise RuntimeError("Failed to find REDIS_URL in environment variables! Make sure it is set!")

    logging.info(f"Connecting to Redis at {redis_url}...")

    redis_client = redis.from_url(redis_url)

    logging.info("Connected to Redis successfully!")

    repo = RedisCartRepository(redis_client)
    app.dependency_overrides[get_repository] = lambda: repo

    logging.info("Order cart service started on port 8002!")

    yield

    logging.info("Shutting down order cart service...")
    await redis_client.close()
    logging.info("Order cart service shutdown complete!")

app = FastAPI(lifespan=lifespan)

@app.exception_handler(CartBaseException)
async def cart_exception_handler(_, exc: CartBaseException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )

app.include_router(router, prefix="/cart", tags=["cart"])
