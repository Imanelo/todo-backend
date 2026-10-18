import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.storage import task_storage


@pytest.fixture(autouse=True)
def clean_storage():
    """Ensure in-memory storage is empty before and after each test."""
    task_storage.clear()
    yield
    task_storage.clear()


@pytest.fixture
def client():
    """Return FastAPI TestClient."""
    with TestClient(app) as test_client:
        yield test_client

