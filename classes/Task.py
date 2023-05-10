import datetime
import os
import json
from json.decoder import JSONDecodeError

global_id: int = 1
tasks_fn = "subcom_tasks.json"
if os.path.exists(tasks_fn): # note that this is susceptible to a race condition
    with open(tasks_fn, "r") as t:
        try:
            global_id = json.load(t)["global_id"]
        except JSONDecodeError:
            pass

class Task():
    def __init__(self, task_name="None", owner="None", contributors=["None"], \
                 status="Unassigned", description="None", comments="None", increment=True):
        global global_id
        self.task_id: int = global_id
        if increment:
            global_id += 1

        self.task_name: str = task_name
        self.owner: str = owner
        self.contributors: "list[str]" = contributors
        self.creation_date: datetime.date = datetime.date.today()
        self.due_date: datetime.date = self.creation_date
        self.status: str = status

        self.description: str = description
        self.comments: str = comments

    def summary_to_tuple(self):
        return (self.task_id, self.task_name, self.owner, self.due_date)
    
    def contributors_to_str(self):
        return ", ".join(self.contributors)
    
    def to_dict(self):
        res = {
            "task_id": self.task_id,
            "task_name": self.task_name,
            "owner": self.owner,
            "contributors": self.contributors,
            "creation_date": self.creation_date.isoformat(),
            "due_date": self.due_date.isoformat(),
            "status": self.status,
            "description": self.description,
            "comments": self.comments,
        }

        return res

    @staticmethod
    def from_dict(data):
        task = Task(increment=False)
        task.task_id = data["task_id"]
        task.task_name = data["task_name"]
        task.owner = data["owner"]
        task.contributors = data["contributors"]
        task.creation_date = datetime.date.fromisoformat(data["creation_date"])
        task.due_date = datetime.date.fromisoformat(data["due_date"])
        task.status = data["status"]
        task.description = data["description"]
        task.comments = data["comments"]
    
    @staticmethod
    def decrement():
        global global_id
        global_id += -1 
    
    @staticmethod
    def get_global_id():
        return global_id
    

    

