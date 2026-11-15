# added by Din: register, login, refresh and logout endpoints
from fastapi import APIRouter, HTTPException, status

from app.core.security import hash_password
from app.db.fake_db import next_user_id, users_db
from app.schemas.user import UserCreate, UserOut

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate):
    if any(u["username"] == user.username for u in users_db.values()):
        raise HTTPException(status_code=409, detail="Username already taken")
    user_id = next_user_id()
    stored_user = {
        "id": user_id,
        **user.model_dump(exclude={"password"}),
        "hashed_password": hash_password(user.password),  # real bcrypt now
        "is_active": True,
    }
    users_db[user_id] = stored_user
    return stored_user

# added by Din: LOGIN with OAuth2 form, returns JWT access + refresh tokens
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.core.config import auth_settings
from app.core.security import create_access_token, create_refresh_token, verify_password
from app.db.fake_db import refresh_tokens_db
from app.schemas.auth import TokenPair


def make_token_pair(username: str) -> dict:
    """Make a fresh access + refresh token and remember the refresh token."""
    refresh_token = create_refresh_token(username)
    refresh_tokens_db[refresh_token] = username  # save it as VALID
    return {
        "access_token": create_access_token(username),
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # in seconds
    }


@router.post("/login", response_model=TokenPair)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = next((u for u in users_db.values() if u["username"] == form_data.username), None)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Wrong username or password")
    return make_token_pair(user["username"])

# added by Din: REFRESH - swap the old refresh token for a NEW pair (rotation)
import jwt

from app.schemas.auth import RefreshRequest


@router.post("/refresh", response_model=TokenPair)
def refresh(body: RefreshRequest):
    # 1. Is the signature real and is it still in date?
    try:
        payload = jwt.decode(
            body.refresh_token,
            auth_settings.REFRESH_SECRET_KEY,
            algorithms=[auth_settings.ALGORITHM],
        )
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    # 2. Is it really a refresh token (not an access token)?
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Not a refresh token")

    # 3. Is it still on our list? (not used before, not logged out)
    if body.refresh_token not in refresh_tokens_db:
        raise HTTPException(status_code=401, detail="Refresh token already used or revoked")

    # 4. DELETE the old token from the list, then make a NEW pair (which saves the new one)
    username = refresh_tokens_db.pop(body.refresh_token)
    return make_token_pair(username)

# added by Din: WHO AM I - only works with a valid access token
from app.dependencies import get_current_user


@router.get("/me", response_model=UserOut)
def read_me(current_user: dict = Depends(get_current_user)):
    return current_user

# added by Din: LOGOUT - revoke ALL of this user's refresh tokens
from fastapi import Response


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(current_user: dict = Depends(get_current_user)):
    username = current_user["username"]
    for token, owner in list(refresh_tokens_db.items()):
        if owner == username:
            del refresh_tokens_db[token]
    return Response(status_code=status.HTTP_204_NO_CONTENT)