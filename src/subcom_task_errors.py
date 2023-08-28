class TaskNotFoundError(Exception):
    def __init__(self, task_id: int):
        self.task_id = task_id
        self.message = f'Task with ID {self.task_id} does not exist!'
    
    def __str__(self):
        return self.message