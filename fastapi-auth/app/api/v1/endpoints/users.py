from fastapi import APIRouter, Depends, HTTPException, Security, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_token_service, require_roles
from app.core.permissions import Role
from app.core.security import hash_password
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import RoleUpdate, UserRead, UserUpdate
from app.services.token_service import TokenService

router = APIRouter()


# ---------- self-service (scope: me) ----------
@router.get("/me", response_model=UserRead)
async def read_me(user: User = Security(get_current_active_user, scopes=["me"])) -> User:
    return user


@router.patch("/me", response_model=UserRead)
async def update_me(
    data: UserUpdate,
    user: User = Security(get_current_active_user, scopes=["me"]),
    db: Session = Depends(get_db),
    token_service: TokenService = Depends(get_token_service),
) -> User:
    if data.full_name is not None:
        user.full_name = data.full_name
    if data.password is not None:
        user.hashed_password = hash_password(data.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    if data.password is not None:
        token_service.revoke_all_for_user(user.id)  # force re-login after password change
    return user


# ---------- admin / moderator ----------
@router.get("/", response_model=list[UserRead])
async def list_users(
    skip: int = 0,
    limit: int = 50,
    _: User = Security(require_roles(Role.ADMIN, Role.MODERATOR), scopes=["users:read"]),
    db: Session = Depends(get_db),
) -> list[User]:
    return list(db.scalars(select(User).offset(skip).limit(min(limit, 100))))


def _get_user_or_404(db: Session, user_id: int) -> User:
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.patch("/{user_id}/role", response_model=UserRead)
async def change_role(
    user_id: int,
    data: RoleUpdate,
    admin: User = Security(require_roles(Role.ADMIN), scopes=["users:write"]),
    db: Session = Depends(get_db),
    token_service: TokenService = Depends(get_token_service),
) -> User:
    user = _get_user_or_404(db, user_id)
    if user.id == admin.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot change your own role")
    user.role = data.role.value
    db.commit()
    db.refresh(user)
    token_service.revoke_all_for_user(user.id)  # old tokens carry old scopes
    return user


@router.patch("/{user_id}/deactivate", response_model=UserRead)
async def deactivate_user(
    user_id: int,
    admin: User = Security(require_roles(Role.ADMIN), scopes=["users:write"]),
    db: Session = Depends(get_db),
    token_service: TokenService = Depends(get_token_service),
) -> User:
    user = _get_user_or_404(db, user_id)
    if user.id == admin.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot deactivate yourself")
    user.is_active = False
    db.commit()
    db.refresh(user)
    token_service.revoke_all_for_user(user.id)
    return user


@router.patch("/{user_id}/activate", response_model=UserRead)
async def activate_user(
    user_id: int,
    _: User = Security(require_roles(Role.ADMIN), scopes=["users:write"]),
    db: Session = Depends(get_db),
) -> User:
    user = _get_user_or_404(db, user_id)
    user.is_active = True
    db.commit()
    db.refresh(user)
    return user
