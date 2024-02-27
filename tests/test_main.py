from fastapi import status
from .setup import client, session


def test_root(client):
    res = client.get("/")
    assert res.status_code == status.HTTP_200_OK
    assert res.json().get("message") == "Hello World!"
