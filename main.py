from fastapi import FastAPI

from products.routes.api.v1.product import product
from users.routes.api.v1.auth import auth
from users.routes.api.v1.user import user
from fastapi.middleware.cors import CORSMiddleware
from config.allowed_origins import allowed_origins

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(auth)
app.include_router(user)
app.include_router(product)
