from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_token_payload, get_token_service
from app.core.permissions import ScopeError, resolve_scopes
from app.core.security import TokenPayload, hash_password, verify_password
from app.db.session import get_db
from app.models.user import User
from app.schemas.token import RefreshRequest, TokenPair
from app.schemas.user import UserCreate, UserRead
from app.services.token_service import InvalidRefreshToken, TokenService

router = APIRouter()


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, db: Session = Depends(get_db)) -> User:
    if db.scalar(select(User).where(User.email == data.email)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    user = User(email=data.email, full_name=data.full_name, hashed_password=hash_password(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/token", response_model=TokenPair)
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    token_service: TokenService = Depends(get_token_service),
) -> TokenPair:
    """OAuth2 password flow. `username` is the email; `scope` is an optional space-separated list."""
    user = db.scalar(select(User).where(User.email == form.username))
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")

    try:
        scopes = resolve_scopes(user.role, form.scopes)
    except ScopeError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

    return token_service.issue_pair(user.id, user.role, scopes)


@router.post("/refresh", response_model=TokenPair)
async def refresh(
    body: RefreshRequest,
    db: Session = Depends(get_db),
    token_service: TokenService = Depends(get_token_service),
) -> TokenPair:
    """Rotate tokens: the old refresh token (and its access token) are revoked."""
    try:
        payload, old_scopes = token_service.consume_refresh_token(body.refresh_token)
    except InvalidRefreshToken as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc), headers={"WWW-Authenticate": "Bearer"}
        )

    user = db.get(User, int(payload.sub))
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User inactive or not found")

    # Re-check scopes against the user's *current* role (it may have been downgraded).
    try:
        scopes = resolve_scopes(user.role, old_scopes)
    except ScopeError:
        scopes = resolve_scopes(user.role, None)
    return token_service.issue_pair(user.id, user.role, scopes)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    payload: TokenPayload = Security(get_token_payload),
    token_service: TokenService = Depends(get_token_service),
) -> None:
    """Revoke the current access token and its paired refresh token (deletes them from the token store)."""
    token_service.revoke_session(payload)


@router.post("/logout-all", status_code=status.HTTP_204_NO_CONTENT)
async def logout_all(
    user: User = Security(get_current_active_user),
    token_service: TokenService = Depends(get_token_service),
) -> None:
    """Revoke every token of the current user on every device."""
    token_service.revoke_all_for_user(user.id)
