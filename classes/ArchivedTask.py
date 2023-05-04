from classes.Task import Task
import datetime

class ArchivedTask(Task):
    def __init__(self):
        self.archived_date = datetime.time.today()