from fastapi import status


def test_create_vote(authorized_client, test_posts):
    res = authorized_client.post("/votes", json={"post_id": 1, "add_vote": 1})
    assert res.status_code == status.HTTP_201_CREATED


def test_delete_vote(authorized_client, test_posts):
    res = authorized_client.post("/votes", json={"post_id": 1, "add_vote": 0})
    assert res.status_code == status.HTTP_204_NO_CONTENT
