from db.mongo import chat_collection, message_collection
from datetime import datetime
from bson import ObjectId

from utils import serialize_mongo

class MessageService:

    @staticmethod
    async def add_message(data):
        try:
            print(f"Adding message to chat_id: {data.chat_id} with content: {data.content}")
            chat = await chat_collection.find_one({"_id": ObjectId(data.chat_id)})
            if not chat:
                return {"error": "Chat not found"}
            message = {
                "chat_id": data.chat_id,
                "content": data.content,
                "timestamp": datetime.utcnow(),
                "is_deleted": False,
                "metadata": {
                    "tags": data.tags,
                    "status": "sent"
                }
            }

            result = await message_collection.insert_one(message)
            # message["id"] = str(result.inserted_id)
            return serialize_mongo(message)
        except Exception as e:
            print(f"Error adding message: {e}")
            return {"error": "Internal server error"}

    @staticmethod
    async def get_messages(chat_id: str, skip: int, limit: int):
        try:
            chat = await chat_collection.find_one({"_id": ObjectId(chat_id)})
            if not chat:
                return {"error": "Chat not found"}
            cursor = message_collection.find(
                {"chat_id": chat_id, "is_deleted": False}
            ).sort("timestamp", -1).skip(skip).limit(limit)

            messages = []
            async for msg in cursor:
                msg["id"] = str(msg["_id"])
                messages.append(serialize_mongo(msg))

            return messages
        except Exception as e:
            print(f"Error fetching messages: {e}")
            return {"error": "Internal server error"}

    @staticmethod
    async def update_message(message_id: str, content: str):
        try:
            message = await message_collection.find_one({"_id": ObjectId(message_id)})
            if not message:
                return {"error": "Message not found"}

            await message_collection.update_one(
                {"_id": ObjectId(message_id)},
                {"$set": {"content": content}}
            )
            return {"message": "Message updated successfully"}
        except Exception as e:
            print(f"Error updating message: {e}")
            return {"error": "Internal server error"}
    @staticmethod
    async def soft_delete(message_id: str):
        try:
            message = await message_collection.find_one({"_id": ObjectId(message_id)})
            print(f"Soft deleting message with id: {message}")
            if not message:
                return {"error": "Message not found"}
            if message.get("is_deleted", False):
                print(f"Message with id: {message_id} is already deleted")
                return {"error": "Message already deleted"} 
            await message_collection.update_one(
                {"_id": ObjectId(message_id)},
                {"$set": {"is_deleted": True}}
            )
        except Exception as e:
            print(f"Error soft deleting message: {e}")
            return {"error": "Internal server error"}

       

        