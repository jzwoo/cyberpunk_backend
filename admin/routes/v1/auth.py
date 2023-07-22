import os
from dotenv import load_dotenv
from fastapi import APIRouter, Response, Request, Depends
from fastapi.security import HTTPBasicCredentials

from admin.controllers.login_controller import login_controller
from admin.controllers.logout_controller import logout_controller
from admin.jwt.jwt_functions import verify_token
from admin.models.login import LoginSuccessResponse
from config.db import client

load_dotenv()
admin = APIRouter()
# db
connection_db = client[os.getenv('MONGO_DATABASE')]


@admin.post('/api/v1/admin/login', response_description="Admin login", response_model=LoginSuccessResponse)
async def login(credentials: HTTPBasicCredentials, response: Response):
    return login_controller(connection_db, credentials, response)


@admin.post('/api/v1/admin/logout', response_description="Logout")
async def logout(response: Response, requester=Depends(verify_token)):
    return logout_controller(connection_db, response, requester)


@admin.get('/api/v1/admin/refresh', response_description="Refresh", response_model=LoginSuccessResponse)
async def refresh(request: Request, response: Response):
    return refresh_controller(connection_db, request, response)
