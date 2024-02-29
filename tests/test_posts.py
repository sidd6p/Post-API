from fastapi import status
from app.schemas import PostResponseBase


def test_create_post(authorized_client):
    res = authorized_client.post(
        "/posts",
        json={"title": "Test Post", "content": "This is Test Post", "published": False},
    )
    new_post = PostResponseBase(**res.json())
    assert res.status_code == status.HTTP_201_CREATED


def test_get_post_by_id(client, test_posts):
    res = client.get("/posts/3")
    post = PostResponseBase(**res.json())
    assert res.status_code == status.HTTP_200_OK


def test_get_posts(client, test_posts):
    res = client.get("/posts")
    posts = PostResponseBase(**res.json()[0])
    assert res.status_code == status.HTTP_200_OK


def test_delete_post(authorized_client, test_posts):
    res = authorized_client.delete("/posts/1")
    assert res.status_code == status.HTTP_204_NO_CONTENT


def test_update_post(authorized_client, test_posts):
    res = authorized_client.put(
        "/posts/2",
        json={"title": "Updated Post 1", "content": "Updated This is Post 111"},
    )
    updated_post = PostResponseBase(**res.json())
    assert res.status_code == status.HTTP_200_OK
