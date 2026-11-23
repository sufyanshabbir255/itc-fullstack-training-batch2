from fastapi import FastAPI
from sqlalchemy.orm import Session

from app.database import (
    Base
    ,engine
    ,SessionLocal
)

from app.schemas import (
    UserCreate,
    PostCreate
)

from app.models import (
    User,
    Post
)



app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {
        "message": "Running"
    }


@app.post("/users")
def create_user(user: UserCreate):

    db: Session = SessionLocal()

    new_user = User(
        username=user.username,
        email=user.email,
        password=user.password
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return new_user


@app.post("/posts")
def create_post(post: PostCreate):

    db: Session = SessionLocal()

    new_post = Post(
        title=post.title,
        content=post.content,
        user_id=post.user_id
    )

    db.add(new_post)

    db.commit()

    db.refresh(new_post)

    return new_post

@app.get("/posts")
def get_posts():

    db: Session = SessionLocal()

    posts = db.query(Post).all()

    return posts

@app.get("/users/{user_id}/posts")
def get_user_posts(user_id: int):

    db: Session = SessionLocal()

    posts = (
        db.query(Post)
        .filter(Post.user_id == user_id)
        .all()
    )

    return posts