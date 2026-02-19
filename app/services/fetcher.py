import httpx
from typing import Dict, Any
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


async def fetch_metadata(url: str) -> Dict[str, Any]:
    try:
        async with httpx.AsyncClient(timeout=settings.REQUEST_TIMEOUT) as client:
            response = await client.get(url)

        logger.info(f"Fetched metadata for {url}")

        return {
            "url": url,
            "headers": dict(response.headers),
            "cookies": dict(response.cookies),
            "page_source": response.text,
        }

    except httpx.RequestError as exc:
        logger.error(f"Request failed for {url}: {exc}")
        raise
