from classes.Task import Task
from db.db import create_task, get_tasks, clear_all_tasks

def new_task(owner: str, task_name: str = "None") -> Task:
    task = Task(task_name, owner)
    create_task(task)
    return task

def view_task(task_id: int) -> Task:
    pass

def view_all_tasks(view_archive: bool = False) -> "list[Task]":
    return get_tasks()

def archive_task(task_id: int) -> None:
    pass

def delete_task(task_id: int) -> None:
    pass

def clear():
    clear_all_tasks()