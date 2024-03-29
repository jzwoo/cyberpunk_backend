import os
from fastapi import APIRouter, Response, Request, Depends
from fastapi.security import HTTPBasicCredentials
from config.db import client
from users.controllers.login_controller import login_controller
from users.controllers.logout_controller import logout_controller
from users.controllers.refresh import refresh_controller
from users.jwt.jwt_functions import verify_token
from users.models.login import LoginSuccessResponse

auth = APIRouter()

# db
connection_db = client[os.getenv('MONGO_DATABASE')]


@auth.post('/api/v1/login', response_description="Login", response_model=LoginSuccessResponse)
async def login(credentials: HTTPBasicCredentials, response: Response):
    return login_controller(connection_db, credentials, response)


@auth.post('/api/v1/logout', response_description="Logout")
async def logout(response: Response, requester=Depends(verify_token)):
    return logout_controller(connection_db, response, requester)


@auth.get('/api/v1/refresh', response_description="Refresh", response_model=LoginSuccessResponse)
async def refresh(request: Request, response: Response):
    return refresh_controller(connection_db, request, response)
