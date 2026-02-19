from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)


class MetadataDocument(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    url: str
    headers: Dict[str, Any]
    cookies: Dict[str, Any]
    page_source: str

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
