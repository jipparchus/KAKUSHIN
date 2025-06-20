import pytest
from unittest import mock
import os
import yaml
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.db.dependency import get_db
from backend.db.models import Base


"""
pytest_configure
This function is called before any tests and imports
"""


def pytest_configure():
    """
    Creating mock patches before starting the tests because module imported in conftest.py already need them.
    """
    # Mock backend/config.py load_config function
    config_path = os.path.join(os.path.dirname(__file__), 'test_config.yaml')
    with open(config_path) as f:
        fake_config = yaml.safe_load(f)
    mock_load_config = mock.Mock(return_value=fake_config)
    mock.patch("backend.config.load_config", mock_load_config).start()

    # Mock backend/auth/jwt_utils.py module
    mock.patch(
        "backend.auth.jwt_utils.create_token",
        return_value="mocked_token",
    ).start()

    mock.patch(
        "backend.auth.jwt_utils.decode_token",
        return_value={"user_id": "mocked-id"},
    ).start()


"""
Mocks
"""


@pytest.fixture(autouse=True)
def mock_auth(mocker):
    config_path = os.path.join(os.path.dirname(__file__), 'test_config.yaml')
    # Patch load_config wherever it's imported and used
    patch_paths = [
        'backend.auth.jwt_utils.load_config',
        'backend.core.modules.video_utils.load_config',
        'backend.db.init_rdb.load_config',
        'backend.db.session.load_config',
        'backend.routes.upload.load_config',
    ]

    patches = {}
    for path in patch_paths:
        mock = mocker.patch(path)
        with open(config_path, 'r') as f:
            mock.return_value = yaml.safe_load(f)
            patches[path] = mock
    yield patches


@pytest.fixture(autouse=True)
def mock_jwt_utils(mocker):
    # Patch create_token wherever it's imported and used
    patch_paths = [
        'backend.routes.auth.create_token',
        'backend.auth.dependencies.decode_token',
        'backend.routes.upload.decode_token',
    ]

    patches = {}
    for path in patch_paths:
        name = path.split('.')[-1]
        mock = mocker.patch(path)
        mock.return_value = "mocked" if "create" in name else {"user_id": "mocked-id"}
        patches[path] = mock
    yield patches


@pytest.fixture(scope="session")
def app():
    """
    FastAPI app fixture
    This fixture provide the FastAPI instance for testing.
    """
    from backend.main import app as real_app
    return real_app


# Fixture: test sqlalchemy engine
@pytest.fixture(autouse=True)
def engine():
    # Test DB configuration — SQLite in-memory
    SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
    # Create engine and session
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},  # required for sqlite
        poolclass=StaticPool,  # Needed to persist DB across sessions
        echo=False,
    )
    yield engine


# Fixture: test database session
@pytest.fixture(scope="function")
def db(engine):
    TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


# Fixture: test client using shared db fixture
@pytest.fixture(scope="function")
def client(app, db):
    def override_get_db():
        """
        Dependency override
        Replace the backend.dependency.get_db() with a test version that points to the test database.
        """
        yield db
    # Telling FastAPI that whenever Depends(get_db) is called, it should use override_get_db instead.
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
