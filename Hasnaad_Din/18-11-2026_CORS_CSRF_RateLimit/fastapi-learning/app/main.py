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
from fastapi import Depends  # added by Din
from app.dependencies import log_request  # added by Din
from fastapi import Request  # added by Din
from fastapi.middleware.cors import CORSMiddleware  # added by Din
import secrets  # added by Din
from fastapi import HTTPException  # added by Din
from fastapi.responses import JSONResponse  # added by Din
from slowapi import Limiter, _rate_limit_exceeded_handler  # added by Din
from slowapi.util import get_remote_address  # added by Din
from slowapi.errors import RateLimitExceeded  # added by Din


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
    dependencies=[Depends(log_request)],  # added by Din: GLOBAL dependency
    # These are the defaults; change them to move or disable docs
    # (e.g. docs_url=None to hide Swagger in production).
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Plug in all versioned routes: /api/v1/items, /api/v1/users
app.include_router(api_router, prefix=settings.API_V1_PREFIX)

# added by Din: simple middleware that adds security headers to EVERY response
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    print(f"BEFORE: {request.method} {request.url.path}")
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    print("AFTER: security headers added")
    return response

# added by Din: CORS - which websites (origins) may call this API from a browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# added by Din: CSRF double-submit check - cookie and header must match
def verify_csrf(request: Request):
    cookie_token = request.cookies.get("csrf_token")
    header_token = request.headers.get("X-CSRF-Token")
    if not cookie_token or cookie_token != header_token:
        raise HTTPException(status_code=403, detail="CSRF token missing or wrong")


# added by Din: rate limiting - count requests per IP address
limiter = Limiter(key_func=get_remote_address) # get_remote_address - counts each IP address
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


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

# added by Din: step 1 of CSRF - give the client a token (in the body AND as a cookie)
@app.get("/csrf-token", tags=["Security"])
def get_csrf_token():
    token = secrets.token_hex(16)
    response = JSONResponse({"csrf_token": token})
    response.set_cookie("csrf_token", token)
    return response


# added by Din: step 2 of CSRF - this endpoint only works if cookie and header match
@app.post("/transfer", tags=["Security"], dependencies=[Depends(verify_csrf)])
def transfer():
    return {"message": "Transfer done - CSRF check passed"}

# added by Din: max 3 requests per minute per IP, the 4th gets 429
@app.get("/limited", tags=["Security"])
@limiter.limit("3/minute")
def limited(request: Request):
    return {"message": "You are within the rate limit"}