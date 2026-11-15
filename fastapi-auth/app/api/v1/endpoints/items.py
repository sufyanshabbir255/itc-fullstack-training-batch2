from fastapi import APIRouter, Depends, HTTPException, Security, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user
from app.core.permissions import Role
from app.db.session import get_db
from app.models.item import Item
from app.models.user import User
from app.schemas.item import ItemCreate, ItemRead

router = APIRouter()

PRIVILEGED = {Role.ADMIN.value, Role.MODERATOR.value}


@router.get("/", response_model=list[ItemRead])
async def list_items(
    user: User = Security(get_current_active_user, scopes=["items:read"]),
    db: Session = Depends(get_db),
) -> list[Item]:
    """Users see their own items; moderators and admins see all."""
    query = select(Item)
    if user.role not in PRIVILEGED:
        query = query.where(Item.owner_id == user.id)
    return list(db.scalars(query))


@router.post("/", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
async def create_item(
    data: ItemCreate,
    user: User = Security(get_current_active_user, scopes=["items:write"]),
    db: Session = Depends(get_db),
) -> Item:
    item = Item(**data.model_dump(), owner_id=user.id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: int,
    user: User = Security(get_current_active_user, scopes=["items:write"]),
    db: Session = Depends(get_db),
) -> None:
    item = db.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    if item.owner_id != user.id and user.role not in PRIVILEGED:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your item")
    db.delete(item)
    db.commit()
