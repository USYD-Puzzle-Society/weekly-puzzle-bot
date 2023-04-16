global_id: int = 1

class Task():
    def __init__(self, task_name = "None", owner = "None", due_date = "None", status = "Unassigned"):
        global global_id
        self.task_id: int = global_id
        global_id += 1

        self.task_name: str = task_name
        self.owner = owner
        self.due_date: str = due_date
        self.status: str = status

    def to_tuple(self):
        return (self.task_id, self.task_name, self.owner, self.due_date, self.status)
