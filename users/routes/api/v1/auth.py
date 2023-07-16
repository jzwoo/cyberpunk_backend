import os
from fastapi import APIRouter, Response
from fastapi.security import HTTPBasicCredentials
from users.config.db import client
from users.controllers.login_controller import login_controller
from users.models.login import LoginSuccessResponse

auth = APIRouter()

# db
connection_db = client[os.getenv('MONGO_DATABASE')]


@auth.post('/api/v1/login', response_description="Login", response_model=LoginSuccessResponse)
async def login(credentials: HTTPBasicCredentials, response: Response):
    return login_controller(connection_db, credentials, response)
