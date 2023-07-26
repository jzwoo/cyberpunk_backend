import os
from bson import ObjectId
from dotenv import load_dotenv
from typing import Mapping, Any
from fastapi import HTTPException
from pymongo.database import Database
from starlette.responses import Response
from starlette.status import HTTP_204_NO_CONTENT

load_dotenv()


def delete_product_controller(db: Database[Mapping[str, Any]], product_id: str, requester):
    if requester['role'] != 'admin':
        raise HTTPException(status_code=403)

    collection = db[os.getenv('MONGO_DATABASE_PRODUCTS_COLLECTION')]

    # check if product exists
    retrieved_product = collection.find_one({'_id': ObjectId(product_id)})
    if not retrieved_product:
        raise HTTPException(status_code=404, detail="Product not found.")

    delete_result = collection.delete_one({'_id': ObjectId(product_id)})
    if delete_result.deleted_count == 1:
        return Response(status_code=HTTP_204_NO_CONTENT)
