import pytest

from fastapi.testclient import TestClient
from fastapi import status

from app.main import app
from app import database
from app.oauth2 import create_access_token
from app import models

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}/{settings.TEST_DB}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

testingSessionLocal = sessionmaker(autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def session():
    database.Base.metadata.drop_all(bind=engine)
    database.Base.metadata.create_all(bind=engine)
    db = testingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def client(session):
    def override_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[database.get_db] = override_db
    yield TestClient(app)


@pytest.fixture(scope="module")
def test_user(client):
    res = client.post(
        "/users", json={"email": "sidd@gmail.com", "password": "12qw!@QW"}
    )
    new_user = res.json()
    new_user["password"] = "12qw!@QW"
    assert res.status_code == status.HTTP_201_CREATED
    yield new_user


@pytest.fixture(scope="module")
def test_token(test_user):
    yield create_access_token({"id": test_user["id"]})


@pytest.fixture(scope="module")
def authorized_client(client, test_token):
    client.headers["Authorization"] = f"Bearer {test_token}"
    yield client


def create_posts(data):
    return models.Post(**data)


@pytest.fixture(scope="module")
def test_posts(test_user, session):
    posts_data = [
        {"title": "Post 1", "content": "Post 1 content", "owner_id": test_user["id"]},
        {"title": "Post 2", "content": "Post 2 content", "owner_id": test_user["id"]},
        {"title": "Post 3", "content": "Post 3 content", "owner_id": test_user["id"]},
        {"title": "Post 4", "content": "Post 4 content", "owner_id": test_user["id"]},
        {"title": "Post 5", "content": "Post 5 content", "owner_id": test_user["id"]},
    ]
    post_map = map(create_posts, posts_data)
    posts = list(post_map)
    session.add_all(posts)
    session.commit()
