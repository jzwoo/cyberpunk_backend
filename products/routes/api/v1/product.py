import os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends

from admin.jwt.jwt_functions import verify_token
from config.db import client
from products.controllers.add_product_controller import add_product_controller
from products.controllers.delete_product_controller import delete_product_controller
from products.controllers.get_product_controller import get_product_controller
from products.controllers.get_products_controller import get_products_controller
from products.controllers.update_product_controller import update_product_controller
from products.models.product import ProductOut, ProductIn, UpdateProduct

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


@product.post('/api/v1/products', response_description="Add new product", response_model=ProductOut)
async def add_product(product_in: ProductIn, requester=Depends(verify_token)):
    return add_product_controller(connection_db, product_in, requester)


@product.delete('/api/v1/products/{product_id}', response_description="Delete existing product")
async def delete_product(product_id: str, requester=Depends(verify_token)):
    return delete_product_controller(connection_db, product_id, requester)


@product.put('/api/v1/products/{product_id}', response_description="Update existing product",
             response_model=ProductOut)
async def update_product(updates: UpdateProduct, product_id: str, requester=Depends(verify_token)):
    return update_product_controller(connection_db, updates, product_id, requester)
