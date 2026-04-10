from fastapi import APIRouter
from models.user import CreateUserRequest
from services.user_service import UserService

router = APIRouter(prefix="/users")

@router.post("/")
async def create_user(req: CreateUserRequest):
    return await UserService.create_user(req)

@router.get("/{user_id}")
async def get_user(user_id: str):
    return await UserService.get_user(user_id)