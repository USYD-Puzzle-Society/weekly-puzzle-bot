import datetime

from classes.Task import Task
from db import db

def new_task(owner: str, task_name: str = "None") -> Task:
    """
    Given an owner and an optional task name, add a new Task object to the database and return that object.

    Args:   
        owner: Owner of the task.
        task_name: Name of the task.

    Returns:
        A new Task object
    """
    task = Task(owner=owner, task_name=task_name)
    task = db.create_task(task)
    return task

def view_task(task_id: int) -> Task:
    """
    Given a task id, retrieve the corresponding Task.

    Args:
        task_id: id of the task being viewed.
    
    Returns:
        The Task object with the matching id.

    Raises:
        TaskNotFoundError: if there are no Task with a matching id.
    """

    task = db.retrieve_task_by_id(task_id)
    return task

def view_all_tasks(view_archive: bool = False) -> "list[Task]":
    """
    Retrieve all archived or unarchived Task objects.

    Args:
        view_archive: if True, return all Task where Task.archived == True. 
          Otherwise, return all Task where Task.archived == False
        
    Returns:
        A list of Tasks that fulfills the condition.
    """
    tasks = db.retrieve_tasks()
    tasks = list(filter(lambda task: task.archived == view_archive, tasks))
    return tasks

def archive_task(task_id: int) -> None:
    """
    Given a task id, archive the corresponding Task.
    Note that this does not update all existing Task objects! Use view_task to get an updated Task object.

    Args:
        task_id: id of the task being archived.

    Raises:
        TaskNotFoundError: if there are no Task with a matching id.
    """
    task = db.retrieve_task_by_id(task_id)
    task.archived = True
    task.archived_date = datetime.date.today()
    db.update_task(task_id, task)

def delete_task(task_id: int) -> None:
    """
    Given a task id, delete the corresponding Task, regardless of whether it's archived or not.

    Args:
        task_id: id of the task being deleted.

    Raises: TaskNotFoundError: if there are no Task with a matching id.
    """
    db.delete_task(task_id)

def clear():
    db.clear_all_tasks()
    db.clear_task_id_counter()