from fastapi import status


def test_root(client):
    res = client.get("/")
    assert res.status_code == status.HTTP_200_OK
    assert res.json().get("message") == "Hello World!"
