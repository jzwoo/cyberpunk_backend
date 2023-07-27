import os

from bson import ObjectId
from dotenv import load_dotenv
from typing import Mapping, Any

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pymongo.database import Database

from admin.models.roles import Roles
from products.models.product import ProductIn

load_dotenv()


def add_product_controller(db: Database[Mapping[str, Any]], product: ProductIn, requester):
    if requester['role'] != Roles.admin:
        raise HTTPException(status_code=403)

    collection = db[os.getenv('MONGO_DATABASE_PRODUCTS_COLLECTION')]

    # check uniqueness of name
    duplicate_product = collection.find_one({'name': product.name})
    if duplicate_product:
        raise HTTPException(status_code=409, detail="Duplicate product name.")

    product_json = jsonable_encoder(product)
    new_product = collection.insert_one(product_json)

    created_product = collection.find_one({'_id': new_product.inserted_id})
    return created_product
