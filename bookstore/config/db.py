import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise Exception("MONGO_URI environment variable not set")

client = MongoClient(MONGO_URI)
db = client["books_db"]
collection = db["books"]
