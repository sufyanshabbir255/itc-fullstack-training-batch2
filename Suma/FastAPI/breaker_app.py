from fastapi import FastAPI,HTTPException
app = FastAPI()
failure_count=0
@app.get("/")
def home():
    return{"message":"circuit breaker"}
@app.get("/payment")
def payment():
    global failure_count
    failure_count+=1
    if failure_count>=3:
     raise HTTPException(
        status_code=503,detail="circuit is open"
    )
    return{"message":"payment success"}
@app.put("/payment")
def payment():
    global failure_count
    failure_count+=1
    if failure_count>=3:
     raise HTTPException(
        status_code=503,detail="circuit is updated"
    )
    return{"message":"payment success"}
@app.delete("/payment")
def payment():
    global failure_count
    failure_count+=1
    if failure_count>=3:
     raise HTTPException(
        status_code=503,detail="circuit is updated"
    )
    return{"message":"payment success"}

