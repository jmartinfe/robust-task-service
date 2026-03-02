class TaskNotFoundException(Exception):
    """Exception raised when a task is not found."""
    def __init__(self, task_id):
        self.task_id = task_id
        super().__init__(f"Task with ID {task_id} not found.")

class StatusTransitionNotAllowedException(Exception):
    """Exception raised when a status transition is not allowed."""
    def __init__(self, current_status, new_status):
        self.current_status = current_status
        self.new_status = new_status
        super().__init__(f"Cannot transition task from {current_status} to {new_status}.")