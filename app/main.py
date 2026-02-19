from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.routes import router
from app.core.logging import setup_logging
from app.db.repository import create_indexes


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    await create_indexes()
    yield


app = FastAPI(
    title="HTTP Metadata Inventory Service",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router)
