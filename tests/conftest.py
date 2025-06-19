import pytest
from unittest import mock
import os
import yaml
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.db.dependency import get_db
from backend.db.models import Base


"""
pytest_configure
This function is called before any tests and imports
"""


def pytest_configure():
    # Mock backend/config.py load_config function
    config_path = os.path.join(os.path.dirname(__file__), 'test_config.yaml')
    with open(config_path) as f:
        fake_config = yaml.safe_load(f)
    mock_load_config = mock.Mock(return_value=fake_config)
    mock.patch("backend.config.load_config", mock_load_config).start()

    # Mock backend/auth/jwt_utils.py module
    # mock_jwt_utils = mock.Mock()
    # mock_jwt_utils.create_token.return_value = "mocked_token"
    # mock_jwt_utils.decode_token.return_value = {"user_id": "mocked-id"}
    mock.patch(
        "backend.auth.jwt_utils.create_token",
        return_value="mocked_token",
    ).start()

    mock.patch(
        "backend.auth.jwt_utils.decode_token",
        return_value={"user_id": "mocked-id"},
    ).start()



    from backend.main import app


"""
Mocks
"""


# @pytest.fixture(autouse=True)
# def mock_auth(mocker):
#     config_path = os.path.join(os.path.dirname(__file__), 'test_config.yaml')

#     # Patch load_config wherever it's imported and used
#     patch_paths = [
#         'backend.auth.jwt_utils.load_config',
#         'backend.core.modules.video_utils.load_config',
#         'backend.db.init_rdb.load_config',
#         'backend.db.session.load_config',
#         'backend.routes.upload.load_config',
#     ]

#     patches = {}
#     for path in patch_paths:
#         mock = mocker.patch(path)
#         with open(config_path, 'r') as f:
#             mock.return_value = yaml.safe_load(f)
#             patches[path] = mock
#     yield patches


# @pytest.fixture(autouse=True)
# def mock_jwt_utils(mocker):
#     # Patch create_token wherever it's imported and used
#     patch_paths = [
#         'backend.routes.auth.create_token',
#         'backend.routes.auth.decode_token',
#         'backend.routes.upload.create_token',
#         'backend.routes.user_info.decode_token',
#     ]

#     patches = {}
#     for path in patch_paths:
#         name = path.split('.')[-1]
#         mock = mocker.patch(path)
#         mock.return_value = "mocked" if "create" in name else {"user_id": "mocked-id"}
#         patches[name] = mock

#     yield patches


# Create FastAPI instance
# app = FastAPI()
# app.include_router(APIRouter(), prefix="/auth")


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
