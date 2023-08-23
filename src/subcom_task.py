import datetime

from classes.Task import Task
from db.db import database
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
    task.task_id = await retrieve_task_id_counter()
    await set_task_id_counter(task.task_id + 1)

    await database.tasks_collection.insert_one(task.to_dict())

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

    task = await database.tasks_collection.find_one({ "task_id": task_id })
    if not task:
        raise TaskNotFoundError(task_id)
    return await create_task_from_document(task)

async def view_all_tasks(view_archive: bool = False) -> "list[Task]":
    """
    Retrieve all archived or unarchived Task objects.

    Args:
        view_archive: if True, return all Task where Task.archived == True. 
          Otherwise, return all Task where Task.archived == False
        
    Returns:
        A list of Tasks that fulfills the condition.
    """
    cursor = database.tasks_collection.find({})
    tasks: "list[Task]" = [await create_task_from_document(doc) for doc in await cursor.to_list(length=None)]
    tasks.sort(key=lambda task: task.task_id)
    tasks = [task for task in tasks if task.archived == view_archive]
    return tasks

async def update_task(task: Task) -> None:
    """
    Given a Task, update the task in the database with the same task_id as the given task.

    Args:
        task: Task object to be updated.
    
    Raises:
        TaskNotFoundError: if there are no Task with a matching id.
    """
    
    result = await database.tasks_collection.update_one({ 'task_id': task.task_id }, { '$set': task.to_dict() })
    if result.matched_count == 0:
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
    result = await database.tasks_collection.update_one(
        { 'task_id': task_id }, 
        { '$set': 
            { 
                'archived': True,
                'archived_date': datetime.date.today().isoformat() 
            }
        }
    )
    if result.matched_count == 0:
        raise TaskNotFoundError(task_id)


async def delete_task(task_id: int) -> None:
    """
    Given a task id, delete the corresponding Task, regardless of whether it's archived or not.

    Args:
        task_id: id of the task being deleted.

    Raises: TaskNotFoundError: if there are no Task with a matching id.
    """
    result = await database.tasks_collection.delete_one({ 'task_id' : task_id })
    if result.deleted_count == 0:
        raise TaskNotFoundError(task_id)

async def clear():
    await database.tasks_collection.drop()
    await database.task_id_counter_collection.drop()

async def retrieve_task_id_counter() -> int:
    """
    Retrieves the current task_id counter. Note that task_id are sequential, and the current
    task_id counter is NOT the higher task_id, but the highest task_id + 1 - or in other words,
    the task_id that the next new task will have.
    
    Returns:
        The current task_id counter.
    """
    task_id_counter = await database.task_id_counter_collection.find_one({})

    if task_id_counter:
        return task_id_counter['task_id']
    else:
        return 1

async def set_task_id_counter(task_id_counter: int) -> None:
    """
    Set the task id counter to the given value.

    Args:
        task_id_counter: the value task id counter will be set to.
    """
    await database.task_id_counter_collection.update_one({}, 
                                          { '$set': { 'task_id': task_id_counter } }, upsert=True)

async def create_task_from_document(doc) -> Task:
    """
    Given a Mongo document, create a Task object from the document's fields.
    """
    task = Task(doc['task_name'], doc['owner'], doc['contributors'], doc['status'],
                doc['description'], doc['comments'], doc['archived'], doc['archived_date'])
    task.task_id = doc['task_id']
    return task