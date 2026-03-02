from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional
from app.domain.task_status import TaskStatus

class TaskCreate(BaseModel):
    title: str

class TaskRead(BaseModel):
    id: UUID
    title: str
    status: TaskStatus
    created_at: datetime
    completed_at: Optional[datetime] = None

class Config:
    form_attributes = True
    orm_mode = True

class TaskUpdateStatus(BaseModel):
    new_status: TaskStatus