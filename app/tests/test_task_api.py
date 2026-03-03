from fastapi.testclient import TestClient
from app.main import app
from app.schemas.task import TaskStatus
from app.db.session import get_db
import pytest


@pytest.fixture()
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

def test_create_task(client):
    response = client.post("/tasks", json={"title": "Test task"})
    assert response.status_code == 201

    data = response.json()
    assert data["title"] == "Test task"
    assert data["status"] == TaskStatus.CREATED.value
    assert data["id"] is not None


def test_get_tasks_empty(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []