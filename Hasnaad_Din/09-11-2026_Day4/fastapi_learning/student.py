from fastapi import APIRouter

router = APIRouter()

@router.get("/student")
def get_student():
    return {"name": "Hasna"}
