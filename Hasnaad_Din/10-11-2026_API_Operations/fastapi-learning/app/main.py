"""
app/main.py
-----------
The ENTRY POINT. This is where the FastAPI application object is created
and all routers are plugged in.

Run it with:
    fastapi dev app/main.py
or:
    uvicorn app.main:app --reload
          ^^^^^^^^ ^^^
          module   variable name of the FastAPI() object below

OPENAPI DOCS (generated automatically – no extra code needed)
    http://127.0.0.1:8000/docs          -> Swagger UI (interactive "Try it out")
    http://127.0.0.1:8000/redoc         -> ReDoc (clean read-only docs)
    http://127.0.0.1:8000/openapi.json  -> the raw OpenAPI 3 spec (JSON)

FastAPI builds that spec from:
    - the title/description/version passed to FastAPI()
    - every route's path, method, summary, description, tags
    - type hints of path/query parameters
    - Pydantic models used for request bodies and response_model
    - status_code and `responses` declarations
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, status

from app.core.config import settings
from app.db.fake_db import seed_data
from app.routers import api_router


# ---------------------------------------------------------------------------
# Lifespan: code that runs once at startup (before yield) and shutdown (after)
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    seed_data()  # load sample items so GET /items isn't empty
    yield
    # shutdown logic (close DB connections, etc.) would go here


# ---------------------------------------------------------------------------
# Tag metadata: adds descriptions to the groups in Swagger UI
# The "name" must match the `tags=[...]` used in the routers.
# ---------------------------------------------------------------------------
tags_metadata = [
    {"name": "Items", "description": "CRUD operations on items. Shows every HTTP method."},
    {"name": "Users", "description": "Shows how `response_model` hides the password."},
    {"name": "Health", "description": "Simple liveness check."},
]

# ---------------------------------------------------------------------------
# The FastAPI application object
# ---------------------------------------------------------------------------
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    openapi_tags=tags_metadata,
    lifespan=lifespan,
    # These are the defaults; change them to move or disable docs
    # (e.g. docs_url=None to hide Swagger in production).
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Plug in all versioned routes: /api/v1/items, /api/v1/users
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


# ---------------------------------------------------------------------------
# Routes can also be defined directly on `app` (no router) – fine for tiny
# things like a root or health endpoint.
# ---------------------------------------------------------------------------
@app.get("/", tags=["Health"], summary="Welcome message")
def root():
    return {"message": "Welcome! Open /docs to explore the API"}


@app.get(
    "/health",
    tags=["Health"],
    status_code=status.HTTP_200_OK,
    summary="Health check",
)
def health():
    return {"status": "ok"}
