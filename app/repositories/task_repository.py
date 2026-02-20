from sqlalchemy.orm import Session
from app.db.models.task import Task
from  uuid import UUID

class TaskRepository:

    def __init__(self, db: Session):
        self.db = db

    def list(self) -> list[Task]:
        return self.db.query(Task).all()

    def get_by_id(self, task_id: UUID) -> Task | None:
        return self.db.get(Task, task_id)

    def create(self, task: Task) -> Task:
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task: Task) -> None:
        self.db.delete(task)
        self.db.commit()

    def update(self, task: Task) -> Task:
        self.db.commit()
        self.db.refresh(task)
        return task