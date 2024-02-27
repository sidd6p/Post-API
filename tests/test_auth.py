from app.schemas import AccessTokenBase
from .setup import client, session, test_user
from fastapi import status


def test_login(client, test_user):
    res = client.post(
        "/auth/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    access_token = AccessTokenBase(**res.json())
    assert res.status_code == status.HTTP_201_CREATED
    assert access_token.type == "bearer"
