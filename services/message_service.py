from db.mongo import chat_collection, message_collection
from datetime import datetime
from bson import ObjectId
import ulid
from utils import serialize_mongo

class MessageService:
    @staticmethod
    async def ask_question(data):
        try:
            print(f"Adding message to chat_id: {data}")
            chat = await chat_collection.find_one({"chat_id": data.chat_id})
            if not chat:
                return {"error": "Chat not found"}
            message_id = str(ulid.new())
            message = {
                "chat_id": data.chat_id,
                "message_id": message_id,
                "message_type": "question",
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
    async def answer_question(data):
        try:
            print(f"Adding answer to chat_id: {data}")
            chat = await chat_collection.find_one({"chat_id": data.chat_id})
            if not chat:        
                return {"error": "Chat not found"}  
            
            parent_message = await message_collection.find_one({"message_id": data.parent_message_id})
            if not parent_message:
                return {"error": "Parent message not found"}
            message_id = str(ulid.new())
            message = { 
                "chat_id": data.chat_id,
                "message_id": message_id,   
                "message_type": "answer",
                "content": data.content,
                "timestamp": datetime.utcnow(),
                "is_deleted": False,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "parent_message_id": data.parent_message_id
            }
            result = await message_collection.insert_one(message)
            return serialize_mongo(message)
        except Exception as e:
            print(f"Error adding answer: {e}")
            return {"error": "Internal server error"}
    
    @staticmethod
    async def get_complete_chat_history(chat_id: str, skip: int, limit: int):
        try:
            # chat = chat_collection.find_one({"chat_id": chat_id})
            # print(f"Chat found: {chat}")
            # if not chat:
            #     return {"error": "Chat not found"}
            cursor =  message_collection.find(
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

       

        