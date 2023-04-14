class Task():
    def __init__(self):
        self.task_name: str = None
        self.owner = None
        self.due_date: str = None
    
    def set_task_name(self, task_name: str) -> None:
        self.task_name = task_name

    def set_owner(self, owner) -> None:
        self.owner = owner
    
    def set_due_date(self, due_date: str) -> None:
        self.due_date = due_date