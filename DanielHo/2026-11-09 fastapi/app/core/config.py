# \core\config.py

"""
app/core/config.py
------------------

Centralized application configuration.

WHY THIS FILE EXISTS

    - Loads values from .env
    - Prevents hard-coded secrets
    - Provides a single source of truth
    - Makes configuration easier to maintain
"""

from pathlib import Path
import os

from dotenv import load_dotenv


# Project Root
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load .env
load_dotenv(BASE_DIR / ".env")


class Settings:

    # -------------------------------------------------------------------------
    # FastAPI
    # -------------------------------------------------------------------------

    APP_NAME: str = os.getenv(
        "APP_NAME",
        "FastAPI Learning Project",
    )

    APP_VERSION: str = os.getenv(
        "APP_VERSION",
        "1.0.0",
    )

    APP_DESCRIPTION: str = (
        "A teaching project demonstrating "
        "FastAPI, PostgreSQL, OAuth2, JWT, "
        "Dependencies, CRUD Operations and OpenAPI."
    )

    API_V1_PREFIX: str = "/api/v1"

    DEBUG: bool = (
        os.getenv(
            "DEBUG",
            "False",
        ).lower() == "true"
    )

    # -------------------------------------------------------------------------
    # PostgreSQL
    # -------------------------------------------------------------------------

    DB_HOST: str = os.getenv(
        "DB_HOST",
        "localhost",
    )

    DB_PORT: int = int(
        os.getenv(
            "DB_PORT",
            5432,
        )
    )

    DB_NAME: str = os.getenv(
        "DB_NAME",
        "fastapi_db",
    )

    DB_USER: str = os.getenv(
        "DB_USER",
        "postgres",
    )

    DB_PASSWORD: str = os.getenv(
        "DB_PASSWORD",
        "postgres",
    )

    DATABASE_URL: str = (
        f"postgresql+psycopg://"
        f"{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}"
        f"/{DB_NAME}"
    )

    # -------------------------------------------------------------------------
    # JWT Authentication
    # -------------------------------------------------------------------------

    SECRET_KEY: str = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError(
            "SECRET_KEY missing from .env"
        )

    ALGORITHM: str = os.getenv(
        "ALGORITHM",
        "HS256",
    )

    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv(
            "ACCESS_TOKEN_EXPIRE_MINUTES",
            30,
        )
    )

    REFRESH_TOKEN_EXPIRE_DAYS: int = int(
        os.getenv(
            "REFRESH_TOKEN_EXPIRE_DAYS",
            7,
        )
    )

    # -------------------------------------------------------------------------
    # API Keys
    # -------------------------------------------------------------------------

    API_KEY: str = os.getenv(
        "API_KEY",
        "my-secret-key",
    )

    ADMIN_API_KEY: str = os.getenv(
        "ADMIN_API_KEY",
        "my-admin-key",
    )

    # -------------------------------------------------------------------------
    # Redis
    # -------------------------------------------------------------------------

    REDIS_HOST: str = os.getenv(
        "REDIS_HOST",
        "localhost",
    )

    REDIS_PORT: int = int(
        os.getenv(
            "REDIS_PORT",
            6379,
        )
    )

    REDIS_DB: int = int(
        os.getenv(
            "REDIS_DB",
            0,
        )
    )


# Shared settings instance
settings = Settings()