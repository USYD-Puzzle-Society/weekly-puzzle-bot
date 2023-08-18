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
    Given a task id, retrieve the corresponding Task, or None if no task with such id exist.

    Args:
        task_id: id of the task being viewed.
    
    Returns:
        The Task object with the matching id.
    """

    task = db.retrieve_task_by_id(task_id)
    return task

def view_all_tasks(view_archive: bool = False) -> "list[Task]":
    """
    Retrieve all archived or unarchived Task objects.

    Args:
        view_archive: if True, return all Task where Task.archived == True. 
          Otherwise, return all Task where Task.archived = false
        
    Returns:
        A list of Tasks that fulfills the condition.
    """
    return db.retrieve_tasks()

def archive_task(task_id: int) -> None:
    """
    Given a task id, archive the corresponding Task.

    Args:
        task_id: id of the task being archived.

    Returns:
        None.
    """
    task = db.retrieve_task_by_id(task_id)
    task.archived = True
    db.update_task(task_id, task)

def delete_task(task_id: int) -> None:
    """
    Given a task id, delete the corresponding Task, regardless of whether it's archived or not.

    Args:
        task_id: id of the task being deleted.

    Returns:
        None.
    """
    db.delete_task(task_id)

def clear():
    db.clear_all_tasks()
    db.clear_task_id_counter()