from fastapi import (
    FastAPI,
    Request,
    Form,
)

from fastapi.templating import Jinja2Templates

from fastapi.responses import (
    RedirectResponse
)

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

templates = Jinja2Templates(
    directory="app/templates"
)

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

@app.get("/signup")
def signup_page(
    request: Request
):
    return templates.TemplateResponse(
        "signup.html",
        {"request": request}
    )

@app.post("/signup")
def signup(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):

    db = SessionLocal()

    user = User(
        username=username,
        email=email,
        password=password
    )

    db.add(user)

    db.commit()

    return RedirectResponse(
        "/login",
        status_code=302
    )


@app.get("/login")
def login_page(
    request: Request
):
    return templates.TemplateResponse(
        "login.html",
        {"request": request}
    )

@app.post("/login")
def login(
    email: str = Form(...),
    password: str = Form(...)
):

    db = SessionLocal()

    user = (
        db.query(User)
        .filter(
            User.email == email,
            User.password == password
        )
        .first()
    )

    if not user:
        return RedirectResponse(
            "/login",
            status_code=302
        )

    return RedirectResponse(
        f"/dashboard/{user.id}",
        status_code=302
    )


@app.get("/dashboard/{user_id}")
def dashboard(
    user_id: int,
    request: Request
):

    db = SessionLocal()

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    posts = (
        db.query(Post)
        .filter(Post.user_id == user_id)
        .all()
    )

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "user": user,
            "posts": posts
        }
    )


@app.get("/posts/create/{user_id}")
def create_post_page(
    user_id: int,
    request: Request
):

    return templates.TemplateResponse(
        "create_post.html",
        {
            "request": request,
            "user_id": user_id
        }
    )


@app.post("/posts/create/{user_id}")
def create_post(
    user_id: int,
    title: str = Form(...),
    content: str = Form(...)
):

    db = SessionLocal()

    post = Post(
        title=title,
        content=content,
        user_id=user_id
    )

    db.add(post)

    db.commit()

    return RedirectResponse(
        f"/dashboard/{user_id}",
        status_code=302
    )