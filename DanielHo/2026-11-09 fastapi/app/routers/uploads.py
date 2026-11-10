from fastapi import APIRouter, Form, UploadFile, File

router = APIRouter(
    prefix  = "/forms"
    tags    = ["Forms & Files"]
)

@router.port("/login")
def login(
     username   : str = Form(...)
    ,password   : str = Form(...)
):
    return {
         "username" : username
        ,"message"  : "Form submitted"
    }

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...)
):
    return {
         "filename"     : file.filename
        ,"content_type" : file.content_type
    }