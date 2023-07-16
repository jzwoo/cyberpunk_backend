from pydantic import BaseModel

from users.models.user import UserOut


class LoginSuccessResponse(BaseModel):
    user: UserOut
    accessToken: str
