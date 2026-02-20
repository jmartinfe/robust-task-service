from app.repositories.task_repository import InMemoryTaskRepository
from app.services.task_service import TaskService

task_repository = InMemoryTaskRepository()
task_service = TaskService(task_repository)

from app.db.session import SessionLocal
from app.repositories.sqlalchemy_task_repository import SqlAlchemyTaskRepository
from app.services.task_service import TaskService

def get_task_service():
    db = SessionLocal()
    try:
        repo = SqlAlchemyTaskRepository(db)
        return TaskService(repo)
    finally:
        db.close()