from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId

def serialize(document):
    document["id"] = str(document.pop("_id"))
    return document

class MessageIn(BaseModel):
    content: str = Field(..., min_length=1, max_length=500)

class MessageOut(BaseModel):
    id: str = Field(..., alias="_id")
    content: str
    timestamp: datetime

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}