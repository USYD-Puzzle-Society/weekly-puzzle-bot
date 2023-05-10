from classes.Task import Task
import datetime

class ArchivedTask(Task):
    def __init__(self, task: Task=None):
        if task:
            self.task_id = task.task_id
            self.task_name = task.task_name
            self.owner = task.owner
            self.contributors = task.contributors
            self.creation_date = task.creation_date
            self.due_date = task.due_date
            self.status = task.status
            self.description = task.description
            self.comments = task.comments

        self.archived_date = datetime.date.today()
    
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
            "archived_date": self.archived_date.isoformat()
        }

        return res

def from_dict(data):
    if "archived_date" in data:
        task = ArchivedTask()
        task.archived_date = datetime.date.fromisoformat(data["archived_date"])
    else:
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

    return task