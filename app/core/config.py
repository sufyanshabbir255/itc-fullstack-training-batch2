"""
app/core/config.py
------------------
Central place for application settings.

WHY THIS FILE EXISTS
    Values like the app title, version and API prefix are used in more than
    one place (main.py, routers, OpenAPI docs). Keeping them in one module
    avoids "magic strings" scattered around the code base.

    In a real project you would usually load these from environment
    variables (e.g. with `pydantic-settings`). We keep it simple here.
"""


class Settings:
    # --- Shown at the top of the OpenAPI docs (/docs and /redoc) ---------
    APP_NAME: str = "FastAPI Learning API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = (
        "A teaching project that demonstrates **APIRouter**, "
        "**path operations** (GET/POST/PUT/PATCH/DELETE), **response_model**, "
        "**status codes** and **OpenAPI docs** in FastAPI.\n\n"
        "Open `/docs` for Swagger UI or `/redoc` for ReDoc."
    )

    # --- Every versioned route is mounted under this prefix -------------
    # e.g. the items router becomes /api/v1/items
    API_V1_PREFIX: str = "/api/v1"


# A single shared instance that the rest of the app imports.
settings = Settings()
