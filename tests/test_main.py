import pytest
from fastapi.testclient import TestClient
# from backend.main import app
from tests.conftest import app

client = TestClient(app)


def test_root():
    response = client.get('/auth')
    assert response.status_code == 200
