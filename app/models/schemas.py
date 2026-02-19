from pydantic import BaseModel, HttpUrl, field_validator
from typing import Dict, Any

class MetadataCreate(BaseModel):
    url: HttpUrl

    @field_validator("url")
    def only_http_https(cls, value):
        if value.scheme not in ("http", "https"):
            raise ValueError("Only http and https URLs are allowed")
        return value

class MetadataResponse(BaseModel):
    url: HttpUrl
    headers: Dict[str, Any]
    cookies: Dict[str, Any]
    page_source: str

class AcceptedResponse(BaseModel):
    status: str
    message: str

class ErrorResponse(BaseModel):
    detail: str
