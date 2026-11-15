from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    PROJECT_NAME: str = "FastAPI JWT Auth"
    API_V1_PREFIX: str = "/api/v1"

    # JWT — use different secrets for access and refresh tokens
    SECRET_KEY: str = "change-me-access-secret"
    REFRESH_SECRET_KEY: str = "change-me-refresh-secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Database
    DATABASE_URL: str = "sqlite:///./app.db"

    # Optional admin bootstrap (created on startup if set)
    FIRST_ADMIN_EMAIL: str | None = None
    FIRST_ADMIN_PASSWORD: str | None = None

    @property
    def access_token_ttl_seconds(self) -> int:
        return self.ACCESS_TOKEN_EXPIRE_MINUTES * 60

    @property
    def refresh_token_ttl_seconds(self) -> int:
        return self.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
