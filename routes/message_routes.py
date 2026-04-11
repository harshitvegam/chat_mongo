from fastapi import APIRouter
from models.message import AskQuestionRequest,AnswerQuestionRequest, CreateMessageRequest, UpdateMessageRequest
from services.message_service import MessageService

router = APIRouter(prefix="/messages")

@router.post("/")
async def create_message(req: CreateMessageRequest):
    return await MessageService.add_message(req)

@router.get("/{chat_id}")
async def get_messages(chat_id: str, skip: int = 0, limit: int = 10):
    return await MessageService.get_messages(chat_id, skip, limit)

@router.put("/{message_id}")
async def update_message(message_id: str, req: UpdateMessageRequest):
   return await MessageService.update_message(message_id, req.content)

@router.post("/question/")
async def add_question(req: AskQuestionRequest):
    return await MessageService.ask_question(req)
@router.post("/answer/")
async def add_answer(req: AnswerQuestionRequest):
    return await MessageService.answer_question(req) 
@router.get("/history/{chat_id}")
async def get_chat_history(chat_id: str, skip: int = 0, limit: int = 10):
    return await MessageService.get_complete_chat_history(chat_id, skip, limit)
@router.delete("/{message_id}")
async def delete_message(message_id: str):
    return await MessageService.soft_delete(message_id)
   