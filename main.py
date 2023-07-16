from fastapi import FastAPI

from users.routes.api.v1.auth import auth
from users.routes.api.v1.user import user

app = FastAPI()

app.include_router(auth)
app.include_router(user)
