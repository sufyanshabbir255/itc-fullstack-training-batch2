# added by Din: ROUTER LEVEL DEPENDENCY - protects EVERY route in this router
from fastapi import APIRouter, Depends

from app.dependencies import check_token
# this code has the check
router = APIRouter(prefix="/secure", tags=["Secure"], dependencies=[Depends(check_token)])


@router.get("/reports")
def get_reports():
    return {"reports": ["Q1 sales", "Q2 sales"]}


@router.get("/settings")
def get_settings():
    return {"theme": "dark"}