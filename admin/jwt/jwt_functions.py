import jwt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

load_dotenv()
SECRET_KEY = os.getenv('ADMIN_JWT_SECRET')
REFRESH_TOKEN_SECRET = os.getenv('ADMIN_REFRESH_TOKEN_SECRET')


def generate_access_token(admin):
    payload = {
        "username": admin['username'],
        "id": str(admin['_id']),
        "iat": datetime.utcnow(),
        # 5 minutes expiration from current
        "exp": datetime.utcnow() + timedelta(minutes=5)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def generate_refresh_token(admin):
    payload = {
        "username": admin['username'],
        "id": str(admin['_id']),
        "iat": datetime.utcnow(),
        # 30 minutes expiration from current
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }

    token = jwt.encode(payload, REFRESH_TOKEN_SECRET, algorithm="HS256")
    return token


def verify_token(token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=["HS256"])

        user = {
            "username": payload['username'],
            "id": payload['id'],
        }

        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
