from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService
from app.schemas.task import TaskCreate, TaskRead

router = APIRouter(prefix="/tasks", tags=["tasks"])

def get_service(db: Session = Depends(get_db)) -> TaskService:
    repository = TaskRepository(db)
    return TaskService(repository)

@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(task_create: TaskCreate, service: TaskService = Depends(get_service)):
    return service.create_task(task_create)