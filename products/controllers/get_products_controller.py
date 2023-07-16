import os
from dotenv import load_dotenv
from typing import Mapping, Any
from pymongo.database import Database

load_dotenv()


def get_products_controller(db: Database[Mapping[str, Any]]):
    products = db[os.getenv('MONGO_DATABASE_PRODUCTS_COLLECTION')].find()
    return products
