from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class CreateMessageRequest(BaseModel):
    chat_id: str
    content: str
    tags: Optional[List[str]] = []

class UpdateMessageRequest(BaseModel):
    content: Optional[str]

class MessageResponse(BaseModel):
    id: str
    chat_id: str
    content: str
    timestamp: datetime
    is_deleted: bool
    metadata: dict