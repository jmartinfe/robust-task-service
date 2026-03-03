from app.repositories.task_repository import TaskRepository
from app.db.models.task import Task
from app.schemas.task import TaskCreate, TaskStatus
from app.services.exceptions import TaskNotFoundException, StatusTransitionNotAllowedException
from uuid import UUID
from datetime import datetime, UTC
import logging

logger = logging.getLogger(__name__)

class TaskService:

    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def create_task(self,data: TaskCreate) -> Task:
        task = Task(title=data.title)
        created_task = self.repository.create(task)

        logger.info(f"Task created with id {created_task.id}")
        return created_task

    def list_tasks(self) -> list[Task]:
        return self.repository.list()

    def get_task(self, task_id: UUID):
        task = self.repository.get_by_id(task_id)
        if not task:
            logger.warning(f"Task with id {task_id} not found")
            raise TaskNotFoundException(task_id)
        return task

    def is_valid_status_transition(self, current_status: TaskStatus, new_status: TaskStatus) -> bool:
        valid_transitions = {
            TaskStatus.CREATED: [TaskStatus.IN_PROGRESS],
            TaskStatus.IN_PROGRESS: [TaskStatus.ON_HOLD, TaskStatus.COMPLETED],
            TaskStatus.ON_HOLD: [TaskStatus.IN_PROGRESS],
            TaskStatus.COMPLETED: []
        }
        return new_status in valid_transitions.get(current_status, [])

    def change_task_status(self, task_id: UUID, new_status: TaskStatus) -> Task:
        task = self.get_task(task_id)
        if task.status == new_status:
            return task
        if not self.is_valid_status_transition(task.status, new_status):
            logger.warning(f"Invalid status transition for task with id {task_id} from {task.status.value} to {new_status.value}")
            raise StatusTransitionNotAllowedException(task.status.value, new_status.value)
        previous_status = task.status
        task.status = new_status
        if (new_status == TaskStatus.COMPLETED):
            task.completed_at = datetime.now(UTC)
        updated_task = self.repository.update(task)

        logger.info(f"Task with id {updated_task.id} status updated from {previous_status.value} to {new_status.value}")
        return updated_task
    
    def delete_task(self, task_id: UUID) -> None:
        task = self.get_task(task_id)
        self.repository.delete(task)
        logger.info(f"Task with id {task_id} deleted")
