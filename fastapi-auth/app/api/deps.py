"""Auth dependencies: OAuth2PasswordBearer, current_user, scopes and roles."""
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.permissions import SCOPES, Role
from app.core.security import TokenPayload, decode_token
from app.db.session import get_db
from app.models.user import User
from app.services.token_service import TokenService

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_PREFIX}/auth/token",
    scopes=SCOPES,
)


def get_token_service(db: Session = Depends(get_db)) -> TokenService:
    return TokenService(db)


async def get_token_payload(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme),
    token_service: TokenService = Depends(get_token_service),
) -> TokenPayload:
    """Decode the bearer token, make sure it is still stored (not revoked), and enforce scopes.

    `security_scopes` collects every scope declared with `Security(..., scopes=[...])`
    anywhere up the dependency chain of the current endpoint.
    """
    authenticate_value = f'Bearer scope="{security_scopes.scope_str}"' if security_scopes.scopes else "Bearer"
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )

    try:
        payload = decode_token(token, expected_type="access")
    except JWTError:
        raise credentials_exc

    if not token_service.is_access_token_active(payload.jti):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked",
            headers={"WWW-Authenticate": authenticate_value},
        )

    missing = [s for s in security_scopes.scopes if s not in payload.scopes]
    if missing:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not enough permissions. Missing scope(s): {', '.join(missing)}",
            headers={"WWW-Authenticate": authenticate_value},
        )
    return payload


async def get_current_user(
    payload: TokenPayload = Security(get_token_payload),
    db: Session = Depends(get_db),
) -> User:
    user = db.get(User, int(payload.sub))
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


async def get_current_active_user(user: User = Security(get_current_user)) -> User:
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    return user


def require_roles(*roles: Role):
    """Role-based access: `Security(require_roles(Role.ADMIN), scopes=["users:write"])`.

    The role is read from the database (not the token) so role changes apply immediately.
    """
    allowed = {r.value for r in roles}

    async def role_checker(user: User = Security(get_current_active_user)) -> User:
        if user.role not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires role: {' or '.join(sorted(allowed))}",
            )
        return user

    return role_checker
