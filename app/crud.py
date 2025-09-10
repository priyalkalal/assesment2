from bson import ObjectId
from bson.errors import InvalidId
from .database import users_collection

def create_user(user: dict) -> str:
    result = users_collection.insert_one(user)
    return str(result.inserted_id)

def get_user(user_id: str) -> dict | None:
    try:
        # Validate ObjectId format first
        obj_id = ObjectId(user_id)
        user = users_collection.find_one({"_id": obj_id})
        if user:
            user["id"] = str(user["_id"])
            del user["_id"]
        return user
    except InvalidId:
        # If the user_id is not a valid ObjectId, return None
        return None