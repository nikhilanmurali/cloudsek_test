import asyncio
from app.services.metadata_service import create_metadata
from app.core.logging import get_logger

logger = get_logger(__name__)


def trigger_background_collection(url: str) -> None:
    logger.info(f"Triggering background collection for {url}")
    asyncio.create_task(create_metadata(url))
