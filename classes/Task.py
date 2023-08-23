import datetime

class Task():
    def __init__(self, task_name="None", owner="None", contributors=["None"],
                 status="Unassigned", description="None", comments="None", archived=False, archived_date=None):
        self.task_id: int = None
        self.task_name: str = task_name
        self.owner: str = owner
        self.contributors: "list[str]" = contributors
        self.creation_date: datetime.date = datetime.date.today()
        self.due_date: datetime.date = self.creation_date
        self.status: str = status

        self.description: str = description
        self.comments: str = comments

        self.archived = archived
        self.archived_date: datetime.date = datetime.date.fromisoformat(archived_date) if archived_date else None

    def summary_to_tuple(self):
        return (self.task_id, self.task_name, self.owner, self.due_date)
    
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
            "archived": self.archived,
            "archived_date": self.archived_date.isoformat() if self.archived_date else None
        }

        return res

    @staticmethod
    def from_dict(data):
        task = Task()
        task.task_id = data["task_id"]
        task.task_name = data["task_name"]
        task.owner = data["owner"]
        task.contributors = data["contributors"]
        task.creation_date = datetime.date.fromisoformat(data["creation_date"])
        task.due_date = datetime.date.fromisoformat(data["due_date"])
        task.status = data["status"]
        task.description = data["description"]
        task.comments = data["comments"]
        task.archived = data["archived"]
        task.archived_date = datetime.date.fromisoformat(data["archived_date"]) if data["archived_date"] else None
        return task
    
    def __eq__(self, other):
        if not isinstance(other, Task):
            return False
        
        return (self.task_id == other.task_id and self.task_name == other.task_name and self.owner == other.owner and 
               self.contributors == other.contributors and self.creation_date == self.creation_date and 
               self.due_date == other.due_date and self.status == other.status and self.description == other.description 
               and self.comments == other.comments)
    

