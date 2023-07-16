import bcrypt
from typing import Mapping, Any
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pymongo.database import Database
from users.models.user import UserIn


def hash_password(plain_password):
    # generate salt
    salt = bcrypt.gensalt()
    # hash password using the salt
    hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def register_controller(db: Database[Mapping[str, Any]], user_in: UserIn):
    collection = db['users']

    # check uniqueness of username
    duplicate_username = collection.find_one({'username': user_in.username})
    if duplicate_username:
        raise HTTPException(status_code=409, detail="Duplicate username.")

    # check uniqueness of email
    duplicate_email = collection.find_one({'email': user_in.email})
    if duplicate_email:
        raise HTTPException(status_code=409, detail="An account with the email has already been registered.")

    # check uniqueness of contact
    duplicate_contact = collection.find_one({'contact': user_in.contact})
    if duplicate_contact:
        raise HTTPException(status_code=409, detail="An account with the contact number has already been registered.")

    # hash password
    user_in.password = hash_password(user_in.password)

    user_json = jsonable_encoder(user_in)
    new_user = collection.insert_one(user_json)

    created_user = collection.find_one({"_id": new_user.inserted_id})
    return created_user
