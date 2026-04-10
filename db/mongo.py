from motor.motor_asyncio import AsyncIOMotorClient

import os
client = AsyncIOMotorClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
db = client.chat_app

user_collection = db.users
chat_collection = db.chats
message_collection = db.messages