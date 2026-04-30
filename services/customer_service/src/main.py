import os
import logging
from contextlib import asynccontextmanager

from models.customer import BaseCustomerTable
from errors.exceptions import CustomerBaseException
from handlers.customer import get_repository, router
from repository.impls.postgres import PostgresCustomerRepository

from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

load_dotenv(override=False)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting customer service...")

    postgres_url = os.getenv("POSTGRES_CUSTOMER_URL")
    if postgres_url is None:
        raise RuntimeError("Failed to find 'POSTGRES_CUSTOMER_URL' in environment variables! Make sure it is set!")

    logging.info(f"Connecting to PostgreSQL at {postgres_url}...")

    engine = create_async_engine(postgres_url, echo=True)
    session_factory = async_sessionmaker(
        engine, 
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with engine.begin() as conn:
        await conn.run_sync(BaseCustomerTable.metadata.create_all)

    app.dependency_overrides[get_repository] = lambda: PostgresCustomerRepository(session_factory())

    logging.info("Customer service started on port 8003!")

    yield

    logging.info("Shutting down customer service...")
    await engine.dispose()
    logging.info("Customer service shutdown complete!")

app = FastAPI(lifespan=lifespan)

@app.exception_handler(CustomerBaseException)
async def customer_exception_handler(_, exc: CustomerBaseException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )

app.include_router(router, prefix="/customers")
