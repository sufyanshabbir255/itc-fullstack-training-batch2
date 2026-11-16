from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/pay")
def make_payment():
    return {"message": "Payment successful"}

