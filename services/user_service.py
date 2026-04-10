from db.mongo import user_collection
from bson import ObjectId

from utils import serialize_mongo

class UserService:

    @staticmethod
    async def create_user(data):
        user = data.dict()
        result = await user_collection.insert_one(user)
        print(f"Inserted user with id: {result} {result.inserted_id}")
        user["id"] = str(result.inserted_id)

        return serialize_mongo(user)

    @staticmethod
    async def get_user(user_id: str):
        user = await user_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return None
        # user["id"] = str(user["_id"])
        return serialize_mongo(user)