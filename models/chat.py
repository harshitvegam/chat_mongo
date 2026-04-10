from pydantic import BaseModel
from datetime import datetime

class CreateChatRequest(BaseModel):
    user_id: str

class ChatResponse(BaseModel):
    chat_id: str
    user_id: str
    is_active: bool
    created_at: datetime