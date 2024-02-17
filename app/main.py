import psycopg2
import time
import os

from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from .database import engine, get_db
from sqlalchemy.orm import Session
from . import model
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

model.Base.metadata.create_all(bind=engine)

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
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def set_post(post: Post, db: Session = Depends(get_db)):
    cursor.execute(
        """ INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
        (
            post.title,
            post.content,
            post.published,
        ),
    )
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get("/posts/{id}", status_code=status.HTTP_200_OK)
async def get_post(id: int, db: Session = Depends(get_db)):
    cursor.execute(""" SELECT * FROM posts WHERE posts.id = %s """, (str(id),))
    post = cursor.fetchone()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found!",
        )
    else:
        return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    cursor.execute(
        """ DELETE FROM posts WHERE posts.id = %s  RETURNING *""", (str(id),)
    )
    deleted_post = cursor.fetchone()
    if deleted_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found!",
        )
    else:
        conn.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
async def update_post(id: int, updated_post: Post, db: Session = Depends(get_db)):
    cursor.execute(
        """ UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
        (
            updated_post.title,
            updated_post.content,
            updated_post.published,
            str(id),
        ),
    )
    updated_post = cursor.fetchone()
    if updated_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found!",
        )
    else:
        conn.commit()
        return {"data": updated_post}
