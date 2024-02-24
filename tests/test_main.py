from fastapi.testclient import TestClient
from app.main import app
from app import database

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.schemas import UserResponse

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}/{settings.TEST_DB}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

testingSessionLocal = sessionmaker(autoflush=False, bind=engine)

database.Base.metadata.create_all(bind=engine)


def override_get_db():
    db = testingSessionLocal()
    try:
        yield db
    finally:
        db.close()


client = TestClient(app)

app.dependency_overrides[database.get_db] = override_get_db


def test_root():
    res = client.get("/")
    assert res.status_code == 200
    assert res.json().get("message") == "Hello World!"


def test_create_user():
    res = client.post(
        "/users", json={"email": "sid12@gmail.com", "password": "12qw!@QW"}
    )
    new_user = UserResponse(**res.json())
    assert res.status_code == 201
    assert new_user.email == "sid12@gmail.com"
