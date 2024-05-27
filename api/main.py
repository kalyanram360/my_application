from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from api.database import SessionLocal
from api.models import Blog 
from api.checkdb import create
from fastapi.staticfiles import StaticFiles
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Event to create the table on startup
create()


app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/create", response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse("create_blog.html", {"request": request})

@app.post("/create_post", response_class=HTMLResponse)
def create_post(request: Request, title: str = Form(...), body: str = Form(...), db: Session = Depends(get_db)):
    new_post = Blog(title=title, body=body)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return "post created"


@app.get("/post/{title}", response_class=HTMLResponse)
def read_post(request: Request, title: str, db: Session = Depends(get_db)):
    post = db.query(Blog).filter(Blog.title == title).first()
    if post is None:
        return {"message": "Post not found"}
    return templates.TemplateResponse("blog.html", {"request": request, "post": post})

@app.get("/titles", response_class=HTMLResponse)
def get_titles(request: Request, db: Session = Depends(get_db)):
    titles = db.query(Blog.title).all()
    return templates.TemplateResponse("choose_title.html", {"request": request, "titles": titles})

@app.get("/delete_post/{title}", response_class=HTMLResponse)
def delete_post(request: Request, title: str, db: Session = Depends(get_db)):
    post = db.query(Blog).filter(Blog.title == title).first()
    if post is None:
        return {"message": "Post not found"}
    db.delete(post)
    db.commit()
    return "post deleted"

@app.get("/titles_for_delete", response_class=HTMLResponse)
def get_titles(request: Request, db: Session = Depends(get_db)):
    titles = db.query(Blog.title).all()
    return templates.TemplateResponse("choose_del_title.html", {"request": request, "titles": titles})
