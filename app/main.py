import psycopg2
import os
import time

from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor


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
    publish: bool = True
    rating: Optional[int] = None


def insert_post(data):
    post_dict = data.model_dump()
    id = randrange(1, 1000000)
    post_dict["id"] = id
    my_posts[id] = post_dict
    return post_dict


def search_post_by_id(id):
    if id in my_posts:
        return my_posts[id]
    else:
        return None


@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"message": "Hello World!"}


@app.get("/posts", status_code=status.HTTP_200_OK)
async def get_posts():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def set_post(post: Post):
    post_dict = insert_post(post)
    return {"data": post_dict}


@app.get("/posts/{id}", status_code=status.HTTP_200_OK)
async def get_post(id: int):
    post = search_post_by_id(id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found!",
        )
    else:
        return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    post = search_post_by_id(id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found!",
        )
    else:
        del my_posts[id]
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
async def update_post(id: int, updated_post: Post):
    post = search_post_by_id(id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found!",
        )
    else:
        my_posts[id] = updated_post
        return {"data": update_post}
