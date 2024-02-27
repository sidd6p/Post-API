from app.schemas import UserResponse
from .setup import client, session
from fastapi import status


def test_create_user(client):
    res = client.post(
        "/users", json={"email": "sidd@gmail.com", "password": "12qw!@QW"}
    )
    new_user = UserResponse(**res.json())
    assert res.status_code == status.HTTP_201_CREATED
    assert new_user.email == "sidd@gmail.com"
