# added by Din: new router for Cookies, Header, Nested Body, Form, File and UploadFile
from fastapi import APIRouter, Cookie, Response

router = APIRouter(prefix="/extras", tags=["Extras"])


# added by Din: COOKIES (1/2) - the server SETS a cookie in the browser
@router.post("/cookies/set", summary="Save a cookie in the browser")
def set_cookie(response: Response, favourite_colour: str):
    response.set_cookie(key="favourite_colour", value=favourite_colour)
    return {"message": f"Cookie saved: favourite_colour = {favourite_colour}"}


# added by Din: COOKIES (2/2) - the server READS the cookie the browser sends back
@router.get("/cookies/read", summary="Read the cookie back")
def read_cookie(favourite_colour: str | None = Cookie(default=None)):
    if favourite_colour is None:
        return {"message": "No cookie found. Call POST /cookies/set first."}
    return {"favourite_colour": favourite_colour}

from fastapi import Header  # added by Din
from app.schemas.order import Order  # added by Din
# added by Din: HEADER - read information the client sends in the request headers
@router.get("/headers", summary="Read request headers")
def read_headers(
    user_agent: str | None = Header(default=None),
    x_token: str | None = Header(default=None),
):
    return {"user_agent": user_agent, "x_token": x_token}

# added by Din: NESTED BODY - the JSON body contains objects and lists inside it
@router.post("/orders", summary="Place an order (nested body)")
def create_order(order: Order):
    total = 0
    for line in order.lines:
        total += line.quantity * line.unit_price
    return {
        "customer": order.customer_name,
        "deliver_to_city": order.delivery_address.city,
        "number_of_lines": len(order.lines),
        "order_total": round(total, 2),
        "tags": order.tags,
    }

from fastapi import File, Form  # added by Din

# added by Din: FORM - data sent like an HTML login form, not as JSON
@router.post("/login", summary="Log in with form fields")
def login(username: str = Form(...), password: str = Form(...)):
    return {"message": f"Welcome {username}!", "password_length": len(password)}


# added by Din: FILE - receive a whole file as raw bytes, plus a form field
@router.post("/files/bytes", summary="Upload a file as bytes")
def upload_bytes(file: bytes = File(...), description: str = Form("")):
    return {"file_size_in_bytes": len(file), "description": description}

from fastapi import UploadFile  # added by Din
# added by Din: UPLOADFILE (1/2) - one file, with its name, type and size
@router.post("/files/upload", summary="Upload a file with UploadFile")
async def upload_file(file: UploadFile):
    contents = await file.read()
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size_in_bytes": len(contents),
    }
