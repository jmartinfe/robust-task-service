from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService
from app.schemas.task import TaskCreate, TaskRead
from uuid import UUID

router = APIRouter(prefix="/tasks", tags=["tasks"])

def get_service(db: Session = Depends(get_db)) -> TaskService:
    repository = TaskRepository(db)
    return TaskService(repository)

@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(task_create: TaskCreate, service: TaskService = Depends(get_service)):
    return service.create_task(task_create)

@router.get("/", response_model=list[TaskRead])
def list_tasks(service: TaskService = Depends(get_service)):
    return service.list_tasks()

@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: UUID, service: TaskService = Depends(get_service)):
    return service.get_task(task_id)

@router.patch("/{task_id}/complete", response_model=TaskRead)
def complete_task(task_id: UUID, service: TaskService = Depends(get_service)):
    return service.complete_task(task_id)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: UUID, service: TaskService = Depends(get_service)):
    service.delete_task(task_id)