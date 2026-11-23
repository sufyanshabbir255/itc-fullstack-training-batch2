# routers/posts.py - a logged-in user creates and lists THEIR posts
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Post, User
from app.schemas import PostCreate, PostRead
from app.security import get_current_user

router = APIRouter(prefix="/api/posts", tags=["posts"])


@router.post("", response_model=PostRead, status_code=201)
def create_post(data: PostCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    post = Post(title=data.title, content=data.content, user_id=user.id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.get("", response_model=list[PostRead])
def my_posts(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Post).filter(Post.user_id == user.id).order_by(Post.id.desc()).all()