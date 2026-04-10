# from app.db.mongo import chat_collection, message_collection
from db.mongo import chat_collection, message_collection
async def create_indexes():

    await chat_collection.create_index("user_id")
    await message_collection.create_index("chat_id")
    await message_collection.create_index("timestamp")