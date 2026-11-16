# added by Din: shapes of the data for login, refresh and logout
from pydantic import BaseModel


class TokenPair(BaseModel):
    """What /login and /refresh send back."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds until the access token expires


class RefreshRequest(BaseModel):
    """What the app sends to /refresh."""
    refresh_token: str