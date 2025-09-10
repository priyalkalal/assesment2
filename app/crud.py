from bson import ObjectId
from .database import users_collection

def create_user(user: dict) -> str:
    result = users_collection.insert_one(user)
    return str(result.inserted_id)

def get_user(user_id: str) -> dict | None:
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        user["id"] = str(user["_id"])
        del user["_id"]
    return user