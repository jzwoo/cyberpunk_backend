from typing import Mapping, Any
from bson import ObjectId
from fastapi import HTTPException
from pymongo.database import Database
from users.models.user import UserUpdate


def update_user_controller(db: Database[Mapping[str, Any]], user_id: str, updates: UserUpdate):
    collection = db['users']

    # check if user exists
    retrieved_user = collection.find_one({"_id": ObjectId(user_id)})
    if retrieved_user is None:
        raise HTTPException(status_code=404, detail="User not found.")

    # filter None values
    to_update = {k: v for k, v in updates.model_dump().items() if v is not None}

    # nothing to update
    if len(to_update) < 1:
        return retrieved_user

    if to_update.keys().__contains__('email'):
        # check uniqueness of email
        duplicate_email = collection.find_one({'email': updates.email})
        if duplicate_email:
            raise HTTPException(status_code=409, detail="An account with the email has already been registered.")

    if to_update.keys().__contains__('contact'):
        # check uniqueness of contact
        duplicate_contact = collection.find_one({'contact': updates.contact})
        if duplicate_contact:
            raise HTTPException(status_code=409,
                                detail="An account with the contact number has already been registered.")

    update_result = collection.update_one({"_id": ObjectId(user_id)}, {"$set": to_update})

    if update_result.modified_count == 1:
        if (updated_user := collection.find_one({"_id": ObjectId(user_id)})) is not None:
            return updated_user
