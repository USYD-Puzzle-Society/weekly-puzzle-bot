from datetime import datetime 
from pydantic import BaseModel
from typing import List, Optional, Tuple

class Task(BaseModel):
    task_id: Optional[int] = None
    task_name: str = "None"
    owner: str = "None"
    contributors: List[str] = ["None"]

    description: str = "None"
    comments: str = "None"

    creation_date: datetime = datetime.now().replace(microsecond=0)
    due_date: Optional[datetime] = None
    archived: bool = False
    archived_date: Optional[datetime] = None

    def get_summary(self) -> Tuple[int, str, str, datetime]: 
        return (self.task_id, self.task_name, self.owner, self.due_date)