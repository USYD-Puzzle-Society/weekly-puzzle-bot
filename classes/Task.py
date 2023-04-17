import datetime

global_id: int = 1

class Task():
    def __init__(self, task_name = "None", owners = ["None"], due_date = datetime.date.today(), status = "Unassigned"):
        global global_id
        self.task_id: int = global_id
        global_id += 1

        self.task_name: str = task_name
        self.owners: "list[str]" = owners
        self.creation_date: datetime.date = datetime.date.today()
        self.due_date: datetime.date = due_date # just in case we support due date on creation eventually
        self.status: str = status

    def to_tuple(self):
        return (self.task_id, self.task_name, self.owners, self.creation_date, self.due_date, self.status)

    def owners_to_str(self):
        return ", ".join(self.owners)
