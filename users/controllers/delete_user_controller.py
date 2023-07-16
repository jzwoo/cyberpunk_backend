import os
from dotenv import load_dotenv
from typing import Mapping, Any
from bson import ObjectId
from fastapi import HTTPException
from pymongo.database import Database
from starlette import status
from starlette.responses import JSONResponse

load_dotenv()


def delete_user_controller(db: Database[Mapping[str, Any]], user_id: str, requester):
    if requester['id'] != user_id:
        raise HTTPException(status_code=403)

    collection = db[os.getenv('mongo_database_users_collection')]

    # check if user exists
    retrieved_user = collection.find_one({"_id": ObjectId(user_id)})
    if retrieved_user is None:
        raise HTTPException(status_code=404, detail="User not found.")

    delete_result = collection.delete_one({"_id": ObjectId(user_id)})
    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)
