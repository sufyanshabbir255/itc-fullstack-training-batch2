# core\auth.py

from fastapi import (
    APIRouter,
    Depends,
)

from fastapi.security import (
    OAuth2PasswordRequestForm,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    return {
        "username": form_data.username,
        "password": form_data.password
    }