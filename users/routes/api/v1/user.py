from fastapi import APIRouter
from users.config.db import client
from users.controllers.delete_user_controller import delete_user_controller
from users.controllers.get_user_controller import get_user_controller
from users.controllers.get_users_controller import get_users_controller
from users.controllers.register_controller import register_controller
from users.controllers.update_user_controller import update_user_controller
from users.models.user import UserOut, UserIn, UserUpdate

import os
from dotenv import load_dotenv

load_dotenv()
user = APIRouter()
# db
connection_db = client[os.getenv('MONGO_DATABASE')]


@user.get('/api/v1/users', response_description="List all users", response_model=list[UserOut])
async def get_all_users():
    return get_users_controller(connection_db)


@user.get('/api/v1/users/{user_id}', response_description="Get user by ID", response_model=UserOut)
async def get_all_users(user_id: str):
    return get_user_controller(connection_db, user_id)


@user.post('/api/v1/users', response_description="Create new user", response_model=UserOut)
async def create_new_user(user_in: UserIn):
    return register_controller(connection_db, user_in)


@user.put('/api/v1/users/{user_id}', response_description="Update existing user", response_model=UserOut)
async def update_user(user_id: str, user_update: UserUpdate):
    return update_user_controller(connection_db, user_id, user_update)


@user.delete('/api/v1/users/{user_id}', response_description="Delete existing user")
async def delete_user(user_id: str):
    return delete_user_controller(connection_db, user_id)
