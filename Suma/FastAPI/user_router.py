from fastapi import APIRouter, Depends
def verify_user():
    print("user verified")
    return "suma"
router=APIRouter(
    dependencies = [Depends(verify_user)]
)
@router.get("/router-profile")
def get_profile():
    return{
        "message":"welcome suma",
        "status":"Router dependency is verified"
    }