import os
from dotenv import load_dotenv
from fastapi import APIRouter

from config.db import client
from products.controllers.get_product_controller import get_product_controller
from products.controllers.get_products_controller import get_products_controller
from products.models.product import ProductOut

load_dotenv()
product = APIRouter()
# db
connection_db = client[os.getenv('MONGO_DATABASE')]


@product.get('/api/v1/products', response_description="Get all products", response_model=list[ProductOut])
async def get_all_products():
    return get_products_controller(connection_db)


@product.get('/api/v1/products/{product_id}', response_description="Get product by ID", response_model=ProductOut)
async def get_product(product_id: str):
    return get_product_controller(connection_db, product_id)
