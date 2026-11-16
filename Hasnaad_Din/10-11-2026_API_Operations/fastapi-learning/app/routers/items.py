"""
app/routers/items.py
--------------------
The main teaching file. Full CRUD for "items" using an APIRouter.

CONCEPTS DEMONSTRATED
    1. APIRouter          – group related routes with a shared prefix/tags
    2. Path operations    – @router.get / post / put / patch / delete
    3. Path parameters    – /items/{item_id}  (with validation via Path)
    4. Query parameters   – ?skip=0&limit=10&in_stock=true (via Query)
    5. Request body       – Pydantic model as a function argument
    6. response_model     – shapes and filters the response
    7. status_code        – 200, 201, 204, 404, 409, 422
    8. HTTPException      – return an error with a status code + message
    9. OpenAPI metadata   – summary, description, tags, responses, deprecated

HTTP METHOD CHEAT SHEET
    GET     read           -> 200 OK
    POST    create         -> 201 Created
    PUT     replace whole  -> 200 OK
    PATCH   change part    -> 200 OK
    DELETE  remove         -> 204 No Content (empty body)
"""

from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Path, Query, Response, status

from app.db.fake_db import items_db, next_item_id
from app.schemas.item import ItemCreate, ItemOut, ItemPatch, ItemUpdate

# ---------------------------------------------------------------------------
# 1. APIRouter
# ---------------------------------------------------------------------------
# prefix    -> every route below starts with /items
# tags      -> groups these routes under "Items" in Swagger UI
# responses -> extra documented responses applied to ALL routes in this router
router = APIRouter(
    prefix="/items",
    tags=["Items"],
    responses={404: {"description": "Item not found"}},
)


# Small helper so we don't repeat the "not found" logic in every route.
def get_item_or_404(item_id: int) -> dict:
    item = items_db.get(item_id)
    if item is None:
        # HTTPException stops the request and returns this JSON:
        #   {"detail": "Item with id 42 not found"}  with status 404
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found",
        )
    return item


# ---------------------------------------------------------------------------
# GET /items  -> list items (with QUERY parameters)
# ---------------------------------------------------------------------------
@router.get(
    "/",
    response_model=list[ItemOut],          # response is a LIST of ItemOut
    status_code=status.HTTP_200_OK,        # 200 is the default, shown for clarity
    summary="List all items",
    description="Returns items with optional pagination and filtering.",
)
def list_items(
    # Any function argument that is NOT in the path and NOT a Pydantic model
    # is treated as a QUERY parameter:  /items?skip=0&limit=10&in_stock=true
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max items to return"),
    in_stock: bool | None = Query(None, description="Filter by stock status"),
):
    results = list(items_db.values())
    if in_stock is not None:
        results = [i for i in results if i["in_stock"] == in_stock]
    return results[skip : skip + limit]


# ---------------------------------------------------------------------------
# GET /items/{item_id}  -> read one item (PATH parameter)
# ---------------------------------------------------------------------------
@router.get(
    "/{item_id}",
    response_model=ItemOut,
    summary="Get a single item",
)
def get_item(
    # {item_id} in the URL maps to this argument. The type hint `int` means
    # FastAPI converts "5" -> 5 and returns 422 if it's not a number.
    # Path(..., gt=0) adds validation and docs.
    item_id: int = Path(..., gt=0, description="The ID of the item"),
):
    return get_item_or_404(item_id)


# ---------------------------------------------------------------------------
# POST /items  -> create (REQUEST BODY + 201 Created)
# ---------------------------------------------------------------------------
@router.post(
    "/",
    response_model=ItemOut,
    status_code=status.HTTP_201_CREATED,   # 201 = a new resource was created
    summary="Create a new item",
    responses={409: {"description": "An item with this name already exists"}},
)
def create_item(item: ItemCreate):
    # Because `item` is a Pydantic model, FastAPI reads it from the JSON BODY,
    # validates it, and returns 422 automatically if it's invalid.

    # Example of a business-rule error -> 409 Conflict
    if any(i["name"].lower() == item.name.lower() for i in items_db.values()):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Item '{item.name}' already exists",
        )

    item_id = next_item_id()
    new_item = {
        "id": item_id,
        **item.model_dump(),                    # Pydantic model -> dict
        "created_at": datetime.now(timezone.utc),
    }
    items_db[item_id] = new_item
    return new_item  # FastAPI converts this dict into ItemOut JSON


# ---------------------------------------------------------------------------
# PUT /items/{item_id}  -> full replace
# ---------------------------------------------------------------------------
@router.put(
    "/{item_id}",
    response_model=ItemOut,
    summary="Replace an item (full update)",
)
def replace_item(item_update: ItemUpdate, item_id: int = Path(..., gt=0)):
    # Path param + body in the same function: FastAPI knows which is which
    # because `item_id` appears in the URL and `item_update` is a model.
    existing = get_item_or_404(item_id)
    updated = {
        "id": item_id,
        **item_update.model_dump(),             # every field is replaced
        "created_at": existing["created_at"],   # keep original timestamp
    }
    items_db[item_id] = updated
    return updated


# ---------------------------------------------------------------------------
# PATCH /items/{item_id}  -> partial update
# ---------------------------------------------------------------------------
@router.patch(
    "/{item_id}",
    response_model=ItemOut,
    summary="Partially update an item",
)
def patch_item(item_patch: ItemPatch, item_id: int = Path(..., gt=0)):
    existing = get_item_or_404(item_id)
    # exclude_unset=True -> only the fields the client ACTUALLY sent.
    # If the client sends {"price": 10}, only price changes.
    changes = item_patch.model_dump(exclude_unset=True)
    existing.update(changes)
    return existing


# ---------------------------------------------------------------------------
# DELETE /items/{item_id}  -> 204 No Content
# ---------------------------------------------------------------------------
@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an item",
    # No response_model: a 204 response must have an EMPTY body.
)
def delete_item(item_id: int = Path(..., gt=0)):
    get_item_or_404(item_id)
    del items_db[item_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ---------------------------------------------------------------------------
# Bonus: a DEPRECATED endpoint (shows as struck-through in Swagger UI)
# ---------------------------------------------------------------------------
@router.get(
    "/search/by-name",
    response_model=list[ItemOut],
    summary="Search items by name (old)",
    deprecated=True,  # OpenAPI marks it deprecated; it still works
)
def search_items_old(q: str = Query(..., min_length=1)):
    return [i for i in items_db.values() if q.lower() in i["name"].lower()]
