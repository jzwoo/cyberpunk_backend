import os

from bson import ObjectId
from dotenv import load_dotenv
from typing import Mapping, Any

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pymongo.database import Database

from admin.models.roles import Roles
from products.models.product import UpdateProduct

load_dotenv()


def update_product_controller(db: Database[Mapping[str, Any]], updates: UpdateProduct, product_id: str, requester):
    if requester['role'] != Roles.admin:
        raise HTTPException(status_code=403)

    collection = db[os.getenv('MONGO_DATABASE_PRODUCTS_COLLECTION')]

    # check if product exists
    retrieved_product = collection.find_one({'_id': ObjectId(product_id)})
    if retrieved_product is None:
        raise HTTPException(status_code=404, detail="Product not found.")

    # TODO: Can optimise update by checking which fields are unchanged
    # filter None values
    to_update = {k: v for k, v in updates.model_dump().items() if v is not None}

    # nothing to update
    if len(to_update) < 1:
        return retrieved_product

    if to_update.keys().__contains__('name'):
        # check uniqueness of name
        duplicate_name = collection.find_one({'name': updates.name})
        if duplicate_name:
            raise HTTPException(status_code=409, detail="There is already another product with the same name.")

    update_result = collection.update_one({"_id": ObjectId(product_id)}, {"$set": to_update})

    if update_result.modified_count == 1:
        if (updated_product := collection.find_one({"_id": ObjectId(product_id)})) is not None:
            return updated_product
