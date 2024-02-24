import pytest

from fastapi.testclient import TestClient
from app.main import app
from app import database

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
