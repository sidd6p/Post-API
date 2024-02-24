from app.schemas import UserResponse, AccessTokenBase
from fastapi import status
from .database import client, session


def test_root(client):
    res = client.get("/")
    assert res.status_code == status.HTTP_200_OK
    assert res.json().get("message") == "Hello World!"


def test_create_user(client):
    res = client.post(
        "/users", json={"email": "sidd@gmail.com", "password": "12qw!@QW"}
    )
    new_user = UserResponse(**res.json())
    assert res.status_code == status.HTTP_201_CREATED
    assert new_user.email == "sidd@gmail.com"


def test_user_login(client):
    res = client.post(
        "/auth/login", data={"username": "sidd@gmail.com", "password": "12qw!@QW"}
    )
    access_token = AccessTokenBase(**res.json())
    assert res.status_code == status.HTTP_201_CREATED
