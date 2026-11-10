from fastapi import APIRouter, Cookie, Header

router = APIRouter(
     prefix ="/client"
    ,tags   =["Headers & Cookies"]
)

@router.get("/headers")
def read_headers(
    user_agent: str | None = Header(
         default        = None
        ,description    = "Browser user agent"
    ),
    host: str | None = Header(default=None)
):
    return {
         "user_agent"   : user_agent
        ,"host"         : host
    }

@router.get("/cookies")
def read_cookies(
    session_id: str | None = Cookie(
         default        = None
        ,description    = "Session Cookie"
    )
):
    return {
        "session_id"    : session_id
    }