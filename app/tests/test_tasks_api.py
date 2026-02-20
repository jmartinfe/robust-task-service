from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_task():
    response = client.post("/tasks", json={"title": "Test task"})
    assert response.status_code == 201

    data = response.json()
    assert data["title"] == "Test task"
    assert data["completed"] is False
    assert data["id"] is not None

def test_get_tasks_empty():
    response = client.get("/tasks")
    assert response.json() == []
    assert response.status_code == 200