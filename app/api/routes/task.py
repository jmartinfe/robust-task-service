from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService
from app.schemas.task import TaskCreate, TaskRead, TaskUpdateStatus
from uuid import UUID
from sqlalchemy import text

router = APIRouter(prefix="/tasks", tags=["tasks"])

def get_service(db: Session = Depends(get_db)) -> TaskService:
    repository = TaskRepository(db)
    return TaskService(repository)

@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.get("/health/ready")
def readiness(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ready"}
    except Exception:
        raise HTTPException(status_code=503, detail="Database not ready")

@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(task_create: TaskCreate, service: TaskService = Depends(get_service)):
    return service.create_task(task_create)

@router.get("/", response_model=list[TaskRead])
def list_tasks(service: TaskService = Depends(get_service)):
    return service.list_tasks()

@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: UUID, service: TaskService = Depends(get_service)):
    return service.get_task(task_id)

@router.patch("/{task_id}/new_status", response_model=TaskRead)
def update_task_status(task_id: UUID, payload: TaskUpdateStatus, service: TaskService = Depends(get_service)):
    return service.change_task_status(task_id, payload.new_status)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: UUID, service: TaskService = Depends(get_service)):
    service.delete_task(task_id)