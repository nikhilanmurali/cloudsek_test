from fastapi import APIRouter, HTTPException, status, responses
from pydantic import HttpUrl

from app.models.schemas import (
    MetadataCreate,
    MetadataResponse,
    AcceptedResponse,
    ErrorResponse,
)
from app.services.metadata_service import (
    create_metadata,
    retrieve_metadata,
)
from app.workers.background import trigger_background_collection
from app.core.logging import get_logger


router = APIRouter(tags=["Metadata"])
logger = get_logger(__name__)


@router.post(
    "/metadata",
    response_model=MetadataResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Failed to fetch metadata",
        },
        422: {
            "model": ErrorResponse,
            "description": "Invalid URL provided",
        },
    },
)
async def create(payload: MetadataCreate):
    """
    Create metadata record for a given URL.
    Fetches headers, cookies, and page source immediately.
    """

    try:
        url_str = str(payload.url)

        metadata = await create_metadata(url_str)

        metadata.pop("_id", None)

        logger.info("metadata_created", url=url_str)

        return metadata

    except Exception as exc:
        logger.error("metadata_creation_failed", url=str(payload.url), error=str(exc))

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to fetch metadata",
        )


@router.get(
    "/metadata",
    response_model=MetadataResponse,
    responses={
        202: {
            "model": AcceptedResponse,
            "description": "Metadata collection started asynchronously",
        },
        422: {
            "model": ErrorResponse,
            "description": "Invalid URL provided",
        },
    },
)
async def get(url: HttpUrl):
    """
    Retrieve metadata for a given URL.

    - Response 200 if metadata exists.
    - Response 202 and triggers background collection if missing.
    - Response 422 if URL is invalid.
    """

    url_str = str(url)

    record = await retrieve_metadata(url_str)

    if record:
        record.pop("_id", None)
        return record

    trigger_background_collection(url_str)

    return responses.JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content={
            "status": "accepted",
            "message": "Metadata collection started",
        },
    )
