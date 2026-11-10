"""
app/routers/users.py
--------------------
A second router, focused on ONE lesson:

    response_model FILTERS OUTPUT.

The stored user dict includes `hashed_password`. We return that whole dict,
but because each route declares `response_model=UserOut`, FastAPI removes
every field that is not in UserOut. The client never sees the password.

Try it: comment out `response_model=UserOut` on create_user, restart, and
POST a user. You will see `hashed_password` leak into the response.
"""

from fastapi import APIRouter, HTTPException, status

from app.db.fake_db import fake_hash_password, next_user_id, users_db
from app.schemas.user import UserCreate, UserOut
from app.schemas.user import UserPatch, UserUpdate  # added by Din
from fastapi import Response  # added by Din: needed later for DELETE's empty reply

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
def create_user(user: UserCreate):
    if any(u["username"] == user.username for u in users_db.values()):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Username already taken"
        )

    user_id = next_user_id()
    stored_user = {
        "id": user_id,
        **user.model_dump(exclude={"password"}),          # drop plain password
        "hashed_password": fake_hash_password(user.password),  # keep hash internally
        "is_active": True,
    }
    users_db[user_id] = stored_user

    # We return the dict WITH hashed_password...
    # ...but response_model=UserOut strips it before sending.
    return stored_user


@router.get("/", response_model=list[UserOut], summary="List users")
def list_users():
    return list(users_db.values())


@router.get("/{user_id}", response_model=UserOut, summary="Get a user")
def get_user(user_id: int):
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

# added by Din: helper so PUT, PATCH and DELETE don't repeat the "not found" check
def get_user_or_404(user_id: int) -> dict:
    user = users_db.get(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

# added by Din: UPDATE (full replace) -> PUT /users/{user_id}
@router.put("/{user_id}", response_model=UserOut, summary="Replace a user")
def replace_user(user_update: UserUpdate, user_id: int):
    existing = get_user_or_404(user_id)
    updated = {
        "id": user_id,
        **user_update.model_dump(exclude={"password"}),
        "hashed_password": fake_hash_password(user_update.password),
        "is_active": existing["is_active"],
    }
    users_db[user_id] = updated
    return updated

# added by Din: UPDATE (partial) -> PATCH /users/{user_id}
@router.patch("/{user_id}", response_model=UserOut, summary="Partially update a user")
def patch_user(user_patch: UserPatch, user_id: int):
    existing = get_user_or_404(user_id)
    changes = user_patch.model_dump(exclude_unset=True)
    if "password" in changes:
        existing["hashed_password"] = fake_hash_password(changes.pop("password"))
    existing.update(changes)
    return existing

# added by Din: DELETE -> DELETE /users/{user_id}
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a user")
def delete_user(user_id: int):
    get_user_or_404(user_id)
    del users_db[user_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)