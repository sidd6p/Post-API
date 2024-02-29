from fastapi import status
from app.schemas import PostResponseBase


def test_create_post(authorized_client):
    res = authorized_client.post(
        "/posts",
        json={"title": "Test Post", "content": "This is Test Post", "published": False},
    )
    new_post = PostResponseBase(**res.json())
    assert res.status_code == status.HTTP_201_CREATED


def test_get_posts(client, test_posts):
    res = client.get("/posts")
    posts = PostResponseBase(**res.json()[0])
    assert res.status_code == status.HTTP_200_OK
