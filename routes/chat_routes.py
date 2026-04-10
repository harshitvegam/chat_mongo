from fastapi import APIRouter
from services.chat_service import ChatService

router = APIRouter(prefix="/chats")

@router.post("/{user_id}")
async def create_chat(user_id: str):
    return await ChatService.create_chat(user_id)

@router.get("/{user_id}")
async def get_chats(user_id: str, skip: int = 0, limit: int = 10):
    return await ChatService.get_chats_by_user(user_id, skip, limit)