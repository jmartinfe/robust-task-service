from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class TaskCreate(BaseModel):
    title: str

class TaskRead(BaseModel):
    id: UUID
    title: str
    completed: bool
    created_at: datetime
    completed_at: Optional[datetime] = None

class Config:
    form_attributes = True