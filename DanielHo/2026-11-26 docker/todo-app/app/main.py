from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.local_db import seed_data
from app.routers import tasks


@asynccontextmanager
async def lifespan(app: FastAPI):
    seed_data()
    yield


app = FastAPI(
    title="To-Do Application",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(tasks.router)


@app.get("/")
def welcome():
    return {
        "message": "Welcome to the To-Do Application"
    }