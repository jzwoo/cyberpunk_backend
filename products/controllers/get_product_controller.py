import os

from bson import ObjectId
from dotenv import load_dotenv
from typing import Mapping, Any

from fastapi import HTTPException
from pymongo.database import Database

load_dotenv()


def get_product_controller(db: Database[Mapping[str, Any]], product_id: str):
    product = db[os.getenv('MONGO_DATABASE_PRODUCTS_COLLECTION')].find_one({'_id': ObjectId(product_id)})

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found.")
    else:
        return product
