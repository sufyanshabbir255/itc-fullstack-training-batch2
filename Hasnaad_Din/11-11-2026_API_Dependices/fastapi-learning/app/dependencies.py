# added by Din: dependencies for the local, router and global examples
from fastapi import Header, HTTPException, Request


# added by Din: LOCAL dependency
def get_greeting():
    return "Hello from a dependency!"


# added by Din: ROUTER dependency
def check_token(x_token: str = Header()):
    if x_token != "secret123":
        raise HTTPException(status_code=401, detail="Invalid token")


# added by Din: GLOBAL dependency
def log_request(request: Request):
    print(f"[Din log] {request.method} {request.url.path}")