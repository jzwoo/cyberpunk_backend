import os
from bson import ObjectId
from typing import Mapping, Any
from pymongo.database import Database
from fastapi import Response


def logout_controller(db: Database[Mapping[str, Any]], response: Response, requester):
    collection = db[os.getenv('mongo_database_admin_collection')]

    retrieved_admin = collection.find_one({"_id": ObjectId(requester['id'])})
    if retrieved_admin:
        # delete token from database
        collection.find_one_and_update(
            {"_id": ObjectId(requester['id'])},
            {'$unset': {"refresh_token": ''}},
        )

    # delete cookie from response
    response.delete_cookie('jwt')
