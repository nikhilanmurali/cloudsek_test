from typing import Optional, Dict, Any
from app.db.client import db

collection = db.metadata

async def create_indexes() -> None:
    await collection.create_index("url", unique=True)


async def get_by_url(url: str) -> Optional[Dict[str, Any]]:
    return await collection.find_one({"url": url})


async def upsert_metadata(data: Dict[str, Any]) -> None:
    await collection.update_one(
        {"url": data["url"]},
        {"$set": data},
        upsert=True,
    )
