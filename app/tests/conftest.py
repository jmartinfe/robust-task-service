import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.services.task_service import TaskService
from app.repositories.task_repository import TaskRepository

TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False,
                                   autoflush=False,
                                   bind=engine)

@pytest.fixture()
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()

    yield session

    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def task_service(db_session):
    repository = TaskRepository(db_session)
    return TaskService(repository)