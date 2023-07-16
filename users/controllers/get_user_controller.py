from typing import Mapping, Any
from bson import ObjectId
from fastapi import HTTPException
from pymongo.database import Database


def get_user_controller(db: Database[Mapping[str, Any]], user_id: str):
    collection = db['users']

    retrieved_user = collection.find_one({"_id": ObjectId(user_id)})
    if retrieved_user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    else:
        return retrieved_user
