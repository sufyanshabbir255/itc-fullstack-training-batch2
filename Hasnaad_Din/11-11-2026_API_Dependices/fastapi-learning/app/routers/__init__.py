"""
app/routers/__init__.py
-----------------------
Combines every feature router into ONE router: `api_router`.

HOW APIRouter NESTING WORKS
    items.router  has prefix "/items"
    users.router  has prefix "/users"

    api_router.include_router(items.router)  -> /items/...
    api_router.include_router(users.router)  -> /users/...

    Then in main.py:
    app.include_router(api_router, prefix="/api/v1")
        -> /api/v1/items/...
        -> /api/v1/users/...

    Prefixes STACK. To release a v2 later, you would create another
    api_router and mount it under "/api/v2" without touching v1.
"""

from fastapi import APIRouter

from app.routers import items, users

api_router = APIRouter()
api_router.include_router(items.router)
api_router.include_router(users.router)

from app.routers import extras  # added by Din
api_router.include_router(extras.router)  # added by Din

from app.routers import secure  # added by Din
api_router.include_router(secure.router)  # added by Din
