from pydantic import BaseModel

from admin.models.admin import AdminOut


class LoginSuccessResponse(BaseModel):
    user: AdminOut
    accessToken: str
