import pytest
import os
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# from backend.main import app
from backend.routes import auth
from backend.db.session import get_db
from backend.db.models import Base

from test_config import test_config


if os.path.exists(test_config['paths']['database']):
    pass
else:
    # Create engine and session
    engine = create_engine(
        test_config['database']['uri'],
        echo=True
    )
    Base.metadata.create_all(engine)

TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


# Create the DB schema
Base.metadata.create_all(bind=engine)


# Create FastAPI instance
app = FastAPI()
app.include_router(auth.router, prefix="/auth")


"""
Dependency override
Replace the backend.dependency.get_db() with a test version that points to the test database.
"""


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Apply override globally before running tests
"""
Telling FastAPI that whenever Depends(get_db) is called, it should use override_get_db instead.
"""
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# Pytest fixture for the client


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c
