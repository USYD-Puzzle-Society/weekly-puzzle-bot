from classes.Task import Task
import datetime

class ArchivedTask(Task):
    def __init__(self, task: Task):
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