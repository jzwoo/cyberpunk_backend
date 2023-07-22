from pydantic import BaseModel

from admin.models.roles import Roles


class Admin(BaseModel):
    username: str
    password: str
    role: Roles


class AdminOut(BaseModel):
    username: str
    role: str
