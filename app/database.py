import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "users_db")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
users_collection = db["users"]
