from pymongo import MongoClient, errors
from pymongo.cursor import Cursor
import os
import sys
from dotenv import load_dotenv
from typing import Union

from classes.Task import Task
from src.subcom_task_errors import TaskNotFoundError

load_dotenv()

uri = os.getenv('DB_URI')

try:
    client = MongoClient(uri)
except errors.ConfigurationError:
    print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
    sys.exit(1)

def retrieve_task_id_counter() -> int:
    """
    Retrieves the current task_id counter. Note that task_id are sequential, and the current
    task_id counter is NOT the higher task_id, but the highest task_id + 1 - or in other words,
    the task_id that the next new task will have.
    
    Returns:
        The current task_id counter.
    """
    db = client['tasks_database']
    task_id_counter_collection = db['id_counter']
    task_id_counter = task_id_counter_collection.find_one({})

    if task_id_counter:
        return task_id_counter['task_id']
    else:
        return 1

def set_task_id_counter(task_id_counter: int) -> None:
    """
    Set the task id counter to the given value.

    Args:
        task_id_counter: the value task id counter will be set to.
    """
    db = client['tasks_database']
    task_id_counter_collection = db['id_counter']
    task_id_counter_collection.update_one({ 'task_id': task_id_counter['task_id'] }, 
                                          { '$set': { 'task_id': task_id_counter } }, upsert=True)


def create_task(task: Task) -> Task:
    """
    Given a Task object, insert it into the database. 
    Update the Task object's task id to the latest task id counter, and increment counter by 1.
    The task will be inserted in the `tasks_database` database, in `tasks` collection

    Args:
        task: the Task object to be inserted.

    Returns:
        The Task object, now with task_id assigned to task_id_counter.
    """
    db = client['tasks_database']
    tasks_collection = db['tasks']

    task.task_id = retrieve_task_id_counter()
    set_task_id_counter(task.task_id + 1)

    tasks_collection.insert_one(task.to_dict())

    return task

def retrieve_task_by_id(task_id: int) -> Task:
    """
    Given a task id, retrieve the corresponding Task from the database.

    Args:
        task_id: id of the task to be searched for.

    Returns: 
        The Task object with the corresponding id.
    
    Raises:
        TaskNotFoundError: if there are no task with the given id.
    """
    db = client['tasks_database']
    tasks_collection = db['tasks']
    cursor: Cursor = tasks_collection.find({ "task_id": task_id })
    results: 'list[Task]' = list(cursor)
    if len(results) == 0:
        raise TaskNotFoundError(task_id)
    return create_task_from_document(results[0])

def retrieve_tasks() -> 'list[Task]':
    """
    Retrieve all tasks from the database, sorted by task id ascending.

    Returns:
        A list of Tasks.
    """
    db = client['tasks_database']
    tasks_collection = db['tasks']
    tasks: "list[Task]" = [create_task_from_document(doc) for doc in tasks_collection.find({})]
    tasks.sort(key=lambda task: task.task_id)
    return tasks

def update_task(task_id: int, task: Task) -> None:
    """
    Given a task id and a task, update all fields of the task with that id to the provided task EXCEPT
    for task id.

    Args:
        task_id: id of the task to be modified.
        task: a Task object that the above task should be updated to.
    
    Raises:
        TaskNotFoundError: if there are no task with the given id.
    """
    db = client['tasks_database']
    tasks_collection = db['tasks']
    task.task_id = task_id
    result = tasks_collection.update_one({ 'task_id': task_id }, { '$set': task.to_dict() })
    if result.matched_count == 0:
        raise TaskNotFoundError(task_id)

def delete_task(task_id: int) -> bool: 
    """
    Given a task id, remove the task corresponding to that id from the database.

    Args:
        task_id: id of the task to be deleted.

    Raises:
        TaskNotFoundError: if there are no task with the given id.
    """
    db = client['tasks_database']
    tasks_collection = db['tasks']
    result = tasks_collection.delete_one({ 'task_id' : task_id })
    return result.deleted_count == 1

def clear_all_tasks() -> None:
    """Remove all tasks from the database."""
    db = client['tasks_database']
    tasks_collection = db['tasks']
    tasks_collection.drop()

def clear_task_id_counter() -> None:
    """Remove task id counter from the database, resetting the counter back to 1."""
    db = client['tasks_database']
    task_id_counter_collection = db['id_counter']
    task_id_counter_collection.drop()

def create_task_from_document(doc) -> Task:
    """
    Given a Mongo document, create a Task object from the document's fields.
    """
    return Task(doc['task_name'], doc['owner'], doc['contributors'], doc['status'],
                doc['description'], doc['comments'])