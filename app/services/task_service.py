from app.repositories.task_repository import TaskRepository
from app.db.models.task import Task
from app.schemas.task import TaskCreate
from app.services.exceptions import TaskNotFoundException
from uuid import UUID
from datetime import datetime, UTC

class TaskService:

    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def create_task(self,data: TaskCreate) -> Task:
        task = Task(title=data.title)
        return self.repository.create(task)

    def list_tasks(self) -> list[Task]:
        return self.repository.list()

    def get_task(self, task_id: UUID):
        task = self.repository.get_by_id(task_id)
        if not task:
            raise TaskNotFoundException(f"Task with id {task_id} not found")
        return task
    
    def complete_task(self, task_id: UUID) -> Task:
        task = self.get_task(task_id)
        task.completed = True
        task.completed_at = datetime.now(UTC)
        return task
