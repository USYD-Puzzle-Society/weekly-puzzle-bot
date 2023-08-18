from pymongo import MongoClient, errors
from pymongo.cursor import Cursor
import os
import sys
from dotenv import load_dotenv
from typing import Union

from classes.Task import Task

load_dotenv()

uri = os.getenv('DB_URI')

try:
    client = MongoClient(uri)
except errors.ConfigurationError:
    print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
    sys.exit(1)

def retrieve_task_id_counter() -> int:
    db = client['tasks_database']
    task_id_counter_collection = db['id_counter']
    task_id_counter = task_id_counter_collection.find_one({})

    if task_id_counter:
        task_id_counter_collection.update_one({ 'task_id': task_id_counter['task_id']}, { '$inc': { 'task_id': 1 } })
        return task_id_counter['task_id']
    else:
        task_id_counter_collection.insert_one({ 'task_id': 2 })
        return 1

def create_task(task: Task) -> Task:
    db = client['tasks_database']
    tasks_collection = db['tasks']

    task.task_id = retrieve_task_id_counter()

    tasks_collection.insert_one(task.to_dict())

    return task

def retrieve_task_by_id(task_id: int) -> Union[Task, None]:
    db = client['tasks_database']
    tasks_collection = db['tasks']
    cursor: Cursor = tasks_collection.find({ "task_id": task_id })
    results: 'list[Task]' = list(cursor)
    if len(results) == 0:
        return None
    return create_task_from_document(results[0])

def retrieve_tasks() -> 'list[Task]':
    db = client['tasks_database']
    tasks_collection = db['tasks']
    tasks: "list[Task]" = [create_task_from_document(doc) for doc in tasks_collection.find({})]
    return tasks

def update_task(task_id: int, task: Task) -> bool:
    db = client['tasks_database']
    tasks_collection = db['tasks']
    result = tasks_collection.update_one({ 'task_id': task_id }, { '$set': task.to_dict() })

    return result.modified_count == 1

def delete_task(task_id: int) -> bool: 
    db = client['tasks_database']
    tasks_collection = db['tasks']
    result = tasks_collection.delete_one({ 'task_id' : task_id })
    return result.deleted_count == 1

def clear_all_tasks() -> None:
    db = client['tasks_database']
    tasks_collection = db['tasks']
    tasks_collection.drop()

def clear_task_id_counter() -> None:
    db = client['tasks_database']
    task_id_counter_collection = db['id_counter']
    task_id_counter_collection.drop()

def create_task_from_document(doc) -> Task:
    return Task(doc['task_name'], doc['owner'], doc['contributors'], doc['status'],
                doc['description'], doc['comments'])