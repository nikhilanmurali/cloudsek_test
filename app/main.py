from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.metadata import router as metadata_router
from app.api.health import router as health_router

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

app.include_router(metadata_router)
app.include_router(health_router)
