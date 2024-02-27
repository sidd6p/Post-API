import pytest
from app.schemas import AccessTokenBase
from fastapi import status


def test_login(client, test_user):
    res = client.post(
        "/auth/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    assert res.status_code == status.HTTP_201_CREATED
    access_token = AccessTokenBase(**res.json())
    assert access_token.type == "bearer"


@pytest.mark.parametrize(
    "email, password",
    [
        ("sidd@gmail.com", "12q"),
        ("sidd1@gmail.com", "12qw!@QW"),
    ],
)
def test_login_failed(client, test_user, email, password):
    res = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": password,
        },
    )
    assert res.status_code == status.HTTP_403_FORBIDDEN
