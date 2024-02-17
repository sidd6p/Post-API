import psycopg2
import time
import os

from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from .database import engine, get_db
from sqlalchemy.orm import Session
from . import models
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

models.Base.metadata.create_all(bind=engine)

load_dotenv()

app = FastAPI()

my_posts = dict()


while True:
    try:
        conn = psycopg2.connect(
            host=os.getenv("HOST"),
            database=os.getenv("DATABASE"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Database connected!")
        break
    except Exception as error:
        print(f"Database connection failed: {error}")
        time.sleep(2)


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"message": "Hello World!"}


@app.get("/posts", status_code=status.HTTP_200_OK)
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def set_post(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


@app.get("/posts/{id}", status_code=status.HTTP_200_OK)
async def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found!",
        )
    else:
        return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found!",
        )
    else:
        post.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
async def update_post(id: int, updated_post: Post, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found!",
        )
    else:
        post.update(updated_post.model_dump(), synchronize_session=False)
        db.commit()
        return {"data": updated_post}
