from fastapi import Header, HTTPException, status

# Local dependency:
# Deleting a user requires an admin API key
def verify_admin(
        x_admin_key: str = Header(...)
):
    if x_admin_key != "secret-admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

# Router dependency:
# Every route in the Users section requires the same security check
def verify_api_key(
        x_api_key: str = Header(...)
):
    if x_api_key != "my-secret-key":
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key"
        )

# Global dependency:
# Every request is logged.
def log_request():
    print("Incoming request")
