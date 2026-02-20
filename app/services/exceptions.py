class TaskNotFoundException(Exception):
    """Exception raised when a task is not found."""
    def __init__(self, task_id):
        self.task_id = task_id
        super().__init__(f"Task with ID {task_id} not found.")

class TaskAlreadyCompletedException(Exception):
    """Exception raised when trying to complete an already completed task."""
    def __init__(self, task_id):
        self.task_id = task_id
        super().__init__(f"Task with ID {task_id} is already completed.")