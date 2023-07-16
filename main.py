from fastapi import FastAPI

from users.routes.api.v1.user import user

app = FastAPI()

app.include_router(user)
