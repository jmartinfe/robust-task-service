from app.schemas.task import TaskCreate, TaskStatus
from app.services.exceptions import StatusTransitionNotAllowedException, TaskNotFoundException
import pytest
import uuid

# Test that creating a task sets the default status to CREATED
def test_create_task_sets_default_status(task_service):
    task = task_service.create_task(TaskCreate(title="Test"))

    assert task.title == "Test"
    assert task.status == TaskStatus.CREATED

# Test valid status transitions
@pytest.mark.parametrize("current_status, new_status",
                         [
                             (TaskStatus.CREATED,TaskStatus.IN_PROGRESS),
                             (TaskStatus.IN_PROGRESS, TaskStatus.ON_HOLD),
                             (TaskStatus.ON_HOLD, TaskStatus.IN_PROGRESS),
                             (TaskStatus.IN_PROGRESS, TaskStatus.COMPLETED)
                             ]
                             )

def test_valid_status_transitions(task_service, current_status, new_status):
    task = task_service.create_task(TaskCreate(title="Test"))

    if current_status != TaskStatus.CREATED:
        task_service.change_task_status(task.id, TaskStatus.IN_PROGRESS)
        if current_status == TaskStatus.ON_HOLD:
            task_service.change_task_status(task.id, TaskStatus.ON_HOLD)

    updated = task_service.change_task_status(task.id, new_status)

    assert updated.status == new_status

# Test invalid status transitions from CREATED
@pytest.mark.parametrize(
        "invalid_status",
        [
            TaskStatus.COMPLETED,
            TaskStatus.ON_HOLD
            ]
            )
def test_invalid_transition_from_created(task_service, invalid_status):
    task = task_service.create_task(TaskCreate(title="Test"))

    with pytest.raises(StatusTransitionNotAllowedException):
        task_service.change_task_status(task.id, invalid_status)

def test_cannot_transition_from_completed(task_service):
    task = task_service.create_task(TaskCreate(title="Test"))
    task_service.change_task_status(task.id, TaskStatus.IN_PROGRESS)
    task_service.change_task_status(task.id, TaskStatus.COMPLETED)

    with pytest.raises(StatusTransitionNotAllowedException):
        task_service.change_task_status(task.id, TaskStatus.IN_PROGRESS)

# Test TaskNotFoundException is raised when trying to change status of a non-existent task
def test_change_status_non_existent_task_raises(task_service):
    fake_id = uuid.uuid4()

    with pytest.raises(TaskNotFoundException):
        task_service.change_task_status(fake_id, TaskStatus.IN_PROGRESS)

# Test TaskNotFoundException is raised when trying to delete a non-existent task
def test_delete_non_existent_task_raises(task_service):
    fake_id = uuid.uuid4()

    with pytest.raises(TaskNotFoundException):
        task_service.delete_task(fake_id)