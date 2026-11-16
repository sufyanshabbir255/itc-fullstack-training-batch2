# core\dependencies.py

"""
app/core/dependencies.py
------------------------

FastAPI dependency examples.

CONCEPTS DEMONSTRATED

    1. Local Dependencies
    2. Router Dependencies
    3. Global Dependencies
    4. OAuth2PasswordBearer
    5. JWT Authentication
    6. Current User Dependency
    7. Role-Based Access Control (RBAC)
    8. Database Session Injection
"""

from fastapi import (
    Depends,
    Header,
    HTTPException,
    status,
)

from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt

from app.core.config import settings
from app.db.database import SessionLocal


# ---------------------------------------------------------------------------
# Local Dependency Example
# ---------------------------------------------------------------------------
# Used only on endpoints that require administrator privileges.
# Example:
#
#   @router.delete(...)
#   def delete_user(
#       _: None = Depends(require_admin)
#   ):
#       ...
# ---------------------------------------------------------------------------

def verify_admin(
    x_admin_key: str = Header(...)
):
    if x_admin_key != settings.ADMIN_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )


# ---------------------------------------------------------------------------
# Router Dependency Example
# ---------------------------------------------------------------------------
# Used on an entire router:
#
# router = APIRouter(
#     prefix="/users",
#     tags=["Users"],
#     dependencies=[Depends(verify_api_key)]
# )
# ---------------------------------------------------------------------------

def verify_api_key(
    x_api_key: str = Header(...)
):
    if x_api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )


# ---------------------------------------------------------------------------
# Global Dependency Example
# ---------------------------------------------------------------------------
# Used in main.py:
#
# app = FastAPI(
#     dependencies=[
#         Depends(log_request)
#     ]
# )
# ---------------------------------------------------------------------------

def log_request():
    print("Incoming request")


# ---------------------------------------------------------------------------
# OAuth2 Scheme
# ---------------------------------------------------------------------------
# Reads:
#
# Authorization: Bearer <token>
# ---------------------------------------------------------------------------

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


# ---------------------------------------------------------------------------
# Database Session Dependency
# ---------------------------------------------------------------------------
# Typical SQLAlchemy dependency.
#
# Usage:
#
# db: Session = Depends(get_db)
# ---------------------------------------------------------------------------

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ---------------------------------------------------------------------------
# JWT Authentication Dependency
# ---------------------------------------------------------------------------
# Decodes the access token and returns the authenticated user.
# ---------------------------------------------------------------------------

def get_current_user(
    token: str = Depends(
        oauth2_scheme
    )
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer"
        },
    )

    try:

        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        email = payload.get("sub")

        if email is None:
            raise credentials_exception

        role = payload.get(
            "role",
            "user"
        )

        return {
            "email": email,
            "role": role
        }

    except JWTError:
        raise credentials_exception


# ---------------------------------------------------------------------------
# Role-Based Access Control (RBAC)
# ---------------------------------------------------------------------------
# Protect administrator-only routes.
#
# Usage:
#
# @router.delete("/{user_id}")
# def delete_user(
#     admin=Depends(require_admin)
# ):
#     ...
# ---------------------------------------------------------------------------

def require_admin(
    current_user=Depends(
        get_current_user
    )
):

    if current_user["role"] != "admin":

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admins only"
        )

    return current_user