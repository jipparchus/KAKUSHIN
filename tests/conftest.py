import pytest
import os
import yaml
from fastapi import FastAPI, APIRouter
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


"""
Mocks
"""


@pytest.fixture(autouse=True)
def mock_auth(mocker):
    mock = mocker.patch('config.config')
    config_path = os.path.join(os.path.dirname(__file__), 'test_config.yaml')
    with open(config_path, 'r') as f:
        mock.return_value = yaml.safe_load(f)
    return mock

from backend.db.dependency import get_db
from backend.db.models import Base

# from test_config import test_config


# Create FastAPI instance
app = FastAPI()
# app.include_router(auth.router, prefix="/auth")
app.include_router(APIRouter(), prefix="/auth")


# Test DB configuration — SQLite in-memory
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
# Create engine and session
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True
)
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


# DB fixture: create/drop tables around each test
@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        """
        Dependency override
        Replace the backend.dependency.get_db() with a test version that points to the test database.
        """
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    # Telling FastAPI that whenever Depends(get_db) is called, it should use override_get_db instead.
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
