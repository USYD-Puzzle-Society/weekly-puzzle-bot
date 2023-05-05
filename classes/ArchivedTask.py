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