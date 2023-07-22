import os
import bcrypt
from dotenv import load_dotenv
from typing import Mapping, Any
from fastapi import HTTPException
from fastapi import Response
from fastapi.security import HTTPBasicCredentials
from pymongo.database import Database

from admin.jwt.jwt_functions import generate_refresh_token, generate_access_token

load_dotenv()


def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def login_controller(db: Database[Mapping[str, Any]], credentials: HTTPBasicCredentials, response: Response):
    collection = db[os.getenv('mongo_database_admin_collection')]

    retrieved_admin = collection.find_one({'username': credentials.username})

    if retrieved_admin is None:
        raise HTTPException(status_code=401)

    if not verify_password(credentials.password, retrieved_admin['password']):
        raise HTTPException(status_code=401)

    refresh_token = generate_refresh_token(retrieved_admin)
    # set the response with a cookie
    response.set_cookie(key='jwt', value=refresh_token, max_age=24 * 60 * 60 * 1000, httponly=True)
    # update the logged in user with a refresh token field to specify logged in
    collection.find_one_and_update(
        {'username': credentials.username},
        {'$set': {"refresh_token": refresh_token}},
    )

    access_token = generate_access_token(retrieved_admin)
    return {'accessToken': access_token, 'user': retrieved_admin}
