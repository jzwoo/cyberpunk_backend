import os
from dotenv import load_dotenv
from typing import Mapping, Any
from bson import ObjectId
from fastapi import HTTPException
from pymongo.database import Database

load_dotenv()


def get_user_controller(db: Database[Mapping[str, Any]], user_id: str):
    collection = db[os.getenv('mongo_database_users_collection')]

    retrieved_user = collection.find_one({"_id": ObjectId(user_id)})
    if retrieved_user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    else:
        return retrieved_user
