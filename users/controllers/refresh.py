import os
import jwt
from dotenv import load_dotenv
from typing import Mapping, Any
from bson import ObjectId
from fastapi import HTTPException, Request, Response
from pymongo.database import Database

from users.jwt.jwt_functions import generate_refresh_token, generate_access_token

load_dotenv()
SECRET_KEY = os.getenv('REFRESH_TOKEN_SECRET')


def refresh_controller(db: Database[Mapping[str, Any]], request: Request, response: Response):
    cookies = request.cookies

    if cookies is None or not cookies.__contains__('jwt'):
        raise HTTPException(status_code=401)

    refresh_token = request.cookies['jwt']
    collection = db[os.getenv('mongo_database_users_collection')]

    try:
        decoded = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
        retrieved_user = collection.find_one({"_id": ObjectId(decoded['id'])})

        if not retrieved_user \
                or not retrieved_user.__contains__('refresh_token') \
                or retrieved_user['refresh_token'] != refresh_token:
            raise HTTPException(status_code=403)

        # regenerate a new refresh token
        refresh_token = generate_refresh_token(retrieved_user)
        response.set_cookie(key='jwt', value=refresh_token, max_age=24 * 60 * 60 * 1000, httponly=True)
        collection.find_one_and_update(
            {"_id": ObjectId(decoded['id'])},
            {'$set': {"refresh_token": refresh_token}},
        )

        # regenerate a access token
        access_token = generate_access_token(retrieved_user)
        return {'accessToken': access_token, 'user': retrieved_user}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
