from db.mongo import chat_collection, user_collection
from datetime import datetime

from utils import serialize_mongo
import ulid
class ChatService:

    @staticmethod
    async def create_chat(user_id: str):
        try:
            user = await user_collection.find_one({"user_id": user_id})
            if not user:
                return {"error": "User not found"}
            # if user.get("is_active", False):
            #     return {"error": "Active chat already exists for this user"}
            chat = {
                "user_id": user_id,
                "chat_id": str(ulid.new()),
                "is_active": True,
                "created_at": datetime.utcnow()
            }

            result = await chat_collection.insert_one(chat)
            # chat["id"] = str(result.inserted_id)
            return serialize_mongo(chat)

        except Exception as e:
            print(f"Error creating chat: {e}")
            return {"error": "Internal server error"}

    @staticmethod
    async def get_chats_by_user(user_id: str, skip: int, limit: int):
        try:
            user = await user_collection.find_one({"user_id": user_id})
            if not user:
                return {"error": "User not found"}
            cursor = chat_collection.find(
                {"user_id": user_id, "is_active": True}
            ).skip(skip).limit(limit)

            chats = []
            async for chat in cursor:
                chat["id"] = str(chat["_id"])

                chats.append(serialize_mongo(chat))

            return chats
        except Exception as e:
            print(f"Error fetching chats: {e}")
            return {"error": "Internal server error"}