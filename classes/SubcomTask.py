from datetime import datetime 
from beanie import Document, Indexed
from typing import List, Optional, Tuple
from pydantic import Field

class Task(Document):
    """A task in the task board.

    Attributes:
        task_id: A sequentially generated integer representing the task's ID. May be omitted, in which case
            it means the task has not been added to the database.
        task_name: A string representing the task's name.
        owner: A string representing the task's owner.
        contributors: A list of string representing the task's contributors.
        description: A string representing the task's description.
        comments: A string representing the task's comments.
        creation_date: A Datetime object representing the creation date of the task. Note that microseconds are set to 0
            due to a limitation in how MongoDB store Datetime.
        due_date: A Datetime object representing the due date of the task.
        archived: A boolean indicating whether the task has been archived.
        archived_date: A Datetime object representing the archival date of the task.
    """
    task_id: Indexed(int) = 1
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
        """
            Retrieve a summary of the task, for use in a task board.

            Returns:
                A tuple consisting of the task ID, task name, owner and due date.
        """
        return (self.task_id, self.task_name, self.owner, self.due_date)
    
class TaskMetadata(Document):
    task_id_counter: int = 1
    archive_channel_id: Optional[int] = None