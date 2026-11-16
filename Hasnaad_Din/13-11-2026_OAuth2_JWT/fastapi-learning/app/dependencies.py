# added by Din: dependencies for the local, router and global examples
from fastapi import Header, HTTPException, Request


# added by Din: LOCAL dependency
def get_greeting():
    return "Hello from a dependency!"


# added by Din: ROUTER dependency
def check_token(x_token: str = Header()):
    if x_token != "secret123":
        raise HTTPException(status_code=401, detail="Invalid token")


# added by Din: GLOBAL dependency
def log_request(request: Request):
    print(f"[Din log] {request.method} {request.url.path}")

# added by Din: CURRENT USER - read and check the JWT access token
import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.core.config import auth_settings
from app.db.fake_db import users_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = jwt.decode(token, auth_settings.SECRET_KEY, algorithms=[auth_settings.ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Access token expired, please refresh")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid access token")
    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Not an access token")
    user = next((u for u in users_db.values() if u["username"] == payload.get("sub")), None)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user