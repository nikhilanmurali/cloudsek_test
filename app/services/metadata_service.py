from typing import Optional, Dict, Any
from app.services.fetcher import fetch_metadata
from app.db.repository import get_by_url, upsert_metadata
from app.core.logging import get_logger

logger = get_logger(__name__)


async def create_metadata(url: str) -> Dict[str, Any]:
    metadata = await fetch_metadata(url)
    await upsert_metadata(metadata)
    logger.info(f"Stored metadata for {url}")
    return metadata


async def retrieve_metadata(url: str) -> Optional[Dict[str, Any]]:
    return await get_by_url(url)
