import os
import jwt
from bson import ObjectId
from dotenv import load_dotenv
from typing import Mapping, Any
from pymongo.database import Database
from fastapi import Request, Response, HTTPException

load_dotenv()
SECRET_KEY = os.getenv('REFRESH_TOKEN_SECRET')


def logout_controller(db: Database[Mapping[str, Any]], request: Request, response: Response):
    cookies = request.cookies

    if cookies is None or not cookies.__contains__('jwt'):
        raise HTTPException(status_code=204)

    refresh_token = request.cookies['jwt']
    collection = db[os.getenv('mongo_database_users_collection')]
    decoded = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])

    retrieved_user = collection.find_one({"_id": ObjectId(decoded['id'])})
    if retrieved_user \
            and retrieved_user.__contains__('refresh_token') \
            and retrieved_user['refresh_token'] == refresh_token:
        # delete token from database
        collection.find_one_and_update(
            {"_id": ObjectId(decoded['id'])},
            {'$unset': {"refresh_token": ''}},
        )

    # delete cookie from response
    response.delete_cookie('jwt')
