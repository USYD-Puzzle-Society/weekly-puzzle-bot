from datetime import datetime
from typing import List
from beanie.exceptions import DocumentNotFound

from classes.SubcomTask import Task, TaskMetadata
from src.subcom_task_errors import TaskNotFoundError

async def new_task(owner: str, task_name: str = "None") -> Task:
    """
    Given an owner and an optional task name, add a new Task object to the database and return that object.

    Args:   
        owner: Owner of the task.
        task_name: Name of the task.

    Returns:
        A new Task object
    """
    task = Task(owner=owner, task_name=task_name)
    await task.save()

    return task

async def view_task(task_id: int) -> Task:
    """
    Given a task id, retrieve the corresponding Task.

    Args:
        task_id: id of the task being viewed.
    
    Returns:
        The Task object with the matching id.

    Raises:
        TaskNotFoundError: if there are no Task with a matching id.
    """

    task = await Task.find(Task.task_id == task_id).first_or_none()
    if not task:
        raise TaskNotFoundError(task_id)
    return task

async def view_all_tasks(view_archive: bool = False) -> List[Task]:
    """
    Retrieve all archived or unarchived Task objects.

    Args:
        view_archive: if True, return all Task where Task.archived == True. 
          Otherwise, return all Task where Task.archived == False
        
    Returns:
        A list of Tasks that fulfills the condition.
    """
    tasks: List[Task] = await Task.find(Task.archived == view_archive).to_list()
    tasks.sort(key=lambda task: task.task_id)
    return tasks

async def update_task(task: Task) -> None:
    """
    Given a Task, update the task in the database with the same task_id as the given task.

    Args:
        task: Task object to be updated.
    
    Raises:
        TaskNotFoundError: if there are no Task with a matching id.
    """
    
    try:
        await task.replace()
    except DocumentNotFound:
        raise TaskNotFoundError(task.task_id)

async def archive_task(task_id: int) -> None:
    """
    Given a task id, archive the corresponding Task.
    Note that this does not update all existing Task objects! Use view_task to get an updated Task object.

    Args:
        task_id: id of the task being archived.

    Raises:
        TaskNotFoundError: if there are no Task with a matching id.
    """
    task = await Task.find(Task.task_id == task_id).first_or_none()
    if not task:
        raise TaskNotFoundError(task_id)
    task.archived = True
    task.archived_date = datetime.now().replace(microsecond=0)
    await task.save()

async def delete_task(task_id: int) -> None:
    """
    Given a task id, delete the corresponding Task, regardless of whether it's archived or not.

    Args:
        task_id: id of the task being deleted.

    Raises: TaskNotFoundError: if there are no Task with a matching id.
    """
    task = await Task.find(Task.task_id == task_id).first_or_none()
    if not task:
        raise TaskNotFoundError(task_id)
    await task.delete()

async def clear():
    await Task.delete_all()
    await TaskMetadata.delete_all()

async def retrieve_task_id_counter() -> int:
    """
    Retrieves the current task_id counter. Note that task_id are sequential, and the current
    task_id counter is NOT the higher task_id, but the highest task_id + 1 - or in other words,
    the task_id that the next new task will have.
    
    Returns:
        The current task_id counter.
    """
    metadata = await TaskMetadata.find_one()

    if metadata:
        return metadata.task_id_counter
    else:
        return 1

async def set_task_id_counter(task_id_counter: int) -> None:
    """
    Set the task id counter to the given value.

    Args:
        task_id_counter: the value task id counter will be set to.
    """
    await TaskMetadata.find_one().upsert(
        {
            '$set': {
                TaskMetadata.task_id_counter: task_id_counter
            }
        }
    )