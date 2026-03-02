from sqlalchemy import Column, String, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base
import uuid
from datetime import datetime, UTC
from app.domain.task_status import TaskStatus

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(UUID(as_uuid=True),
                primary_key=True,
                default=uuid.uuid4)
    title = Column(String, nullable=False)
    status = Column(
        SQLEnum(
            TaskStatus, native_enum=False, length=50),
            nullable=False,
            default=TaskStatus.CREATED)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    completed_at = Column(DateTime(timezone=True), nullable=True)