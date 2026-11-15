"""Roles, OAuth2 scopes and the mapping between them."""
from enum import Enum


class Role(str, Enum):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"


# Every scope the API knows about (shown in the Swagger "Authorize" dialog).
SCOPES: dict[str, str] = {
    "me": "Read and update your own profile",
    "items:read": "Read items",
    "items:write": "Create and delete items",
    "users:read": "List all users",
    "users:write": "Manage users (roles, activation)",
}

# The maximum set of scopes each role may be granted.
ROLE_SCOPES: dict[Role, set[str]] = {
    Role.USER: {"me", "items:read", "items:write"},
    Role.MODERATOR: {"me", "items:read", "items:write", "users:read"},
    Role.ADMIN: set(SCOPES),
}


class ScopeError(ValueError):
    pass


def resolve_scopes(role: Role | str, requested: list[str] | None) -> list[str]:
    """Return the scopes to put in a token.

    - No scopes requested -> grant everything the role allows.
    - Scopes requested -> grant only those, and reject any the role may not have.
    """
    allowed = ROLE_SCOPES[Role(role)]
    if not requested:
        return sorted(allowed)

    unknown = set(requested) - set(SCOPES)
    if unknown:
        raise ScopeError(f"Unknown scope(s): {', '.join(sorted(unknown))}")
    forbidden = set(requested) - allowed
    if forbidden:
        raise ScopeError(f"Scope(s) not allowed for role '{Role(role).value}': {', '.join(sorted(forbidden))}")
    return sorted(set(requested))
