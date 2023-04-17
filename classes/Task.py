import datetime

global_id: int = 1

class Task():
    def __init__(self, task_name="None", owner="None", contributors=["None"], due_date=datetime.date.today(), \
                 status="Unassigned", description="None", comments="None"):
        global global_id
        self.task_id: int = global_id
        global_id += 1

        self.task_name: str = task_name
        self.owner: str = owner
        self.contributors: "list[str]" = contributors
        self.creation_date: datetime.date = datetime.date.today()
        self.due_date: datetime.date = due_date 
        self.status: str = status

        self.description: str = description
        self.comments: str = comments

    def summary_to_tuple(self):
        return (self.task_id, self.task_name, self.owner, self.due_date)
    
    def contributors_to_str(self):
        return ", ".join(self.contributors)
