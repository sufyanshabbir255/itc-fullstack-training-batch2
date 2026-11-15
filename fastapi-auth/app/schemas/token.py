from pydantic import BaseModel


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int          # access token lifetime in seconds
    scope: str               # space-separated granted scopes (OAuth2 style)


class RefreshRequest(BaseModel):
    refresh_token: str
