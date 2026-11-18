from fastapi import FastAPI,Depends
from user_router import router
def verify_global_user():
    print("global dependency verified")
    return True
app = FastAPI(dependencies=[Depends(verify_global_user)])
#app=FastAPI()
app.include_router(router)

print(app.routes)

#simple GET API
@app.get("/hello")
def hello():
    return{"message":"HELLO Suma"}

#simple post api
@app.post("welcome")
def welcome(name:str):
    return{"message":f"welcome{name}"}

#local dependencies
def verify_user():
    return "suma"
@app.get("/profile")
def get_profile(user=Depends(verify_user)):
    return {
        "message":f"welcome{user}",
        "status":"User verified"
    }