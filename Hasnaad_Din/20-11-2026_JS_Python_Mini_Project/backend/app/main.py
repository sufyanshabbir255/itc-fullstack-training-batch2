# main.py - starts the app, creates the tables, and serves the HTML pages
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app import models  # noqa: F401  (import so SQLAlchemy knows the tables)
from app.database import Base, engine
from app.routers import auth, posts

Base.metadata.create_all(bind=engine)  # creates users + posts tables if they don't exist yet

app = FastAPI(title="JS + Python Mini Project")
app.include_router(auth.router)
app.include_router(posts.router)

# serve the frontend folder, so http://localhost:8000 opens index.html (no CORS needed)
app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")