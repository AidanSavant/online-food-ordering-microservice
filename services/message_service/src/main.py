import os
import logging
from pydantic import BaseModel
from contextlib import asynccontextmanager

from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from rabbitmq import publish_msg

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting message queue service...")
    logging.info("Message queue service running on port 8005!")

    yield

    logger.info("Shutting down message queue...")

app = FastAPI(lifespan=lifespan)

class MsgRequest(BaseModel):
    msg: str

@app.post("/send")
async def send_msg(body: MsgRequest) -> JSONResponse:
    logger.info(f"Msg received: {body.msg}")
    message = await publish_msg(body.msg)

    return JSONResponse(content={"message" : message})
