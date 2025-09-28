from fastapi import APIRouter, HTTPException, status
from bson.objectid import ObjectId
from ..database import get_message_collection
from ..models import MessageIn, MessageOut, serialize
from ..ws_manager import manager
from datetime import datetime

router = APIRouter(
    prefix="/messages",
    tags=["Messages"]
)

@router.post("/", response_model=MessageOut, status_code=status.HTTP_201_CREATED)
async def post_message(message: MessageIn):
    message_data = message.model_dump()
    message_data["timestamp"] = datetime.now()
    message_data["room"] = "geral"

    collection = get_message_collection()
    result = await collection.insert_one(message_data)
    
    inserted_document = await collection.find_one({"_id": result.inserted_id})

    message_out = serialize(inserted_document)
    await manager.broadcast(message_out, "geral")
    
    return message_out

@router.get("/", response_model=list[MessageOut])
async def get_messages(before_id: str | None = None):
    collection = get_message_collection()
    query = {"room": "geral"}
    
    if before_id:
        try:
            query["_id"] = {"$lt": ObjectId(before_id)}
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="O parâmetro before_id deve ser um ObjectId válido do MongoDB.")

    cursor = collection.find(query).sort("_id", -1).limit(20)
    messages = [serialize(doc) async for doc in cursor]

    return messages