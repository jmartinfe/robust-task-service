import pytest
from app.dependencies import task_service

@pytest.fixture(autouse=True)
def clear_tasks():
    task_service.clear_tasks()