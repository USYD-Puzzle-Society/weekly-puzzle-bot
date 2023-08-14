import pymongo
import os
import sys
from dotenv import load_dotenv

from classes.Task import Task

load_dotenv()

uri = os.getenv('DB_URI')

try:
    client = pymongo.MongoClient(uri)
except pymongo.errors.ConfigurationError:
    print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
    sys.exit(1)

def create_task(task: Task) -> None:
    db = client['tasks_database']
    tasks_collection = db['tasks']
    tasks_collection.insert_one(task.to_dict())

def get_tasks() -> 'list[Task]':
    db = client['tasks_database']
    tasks_collection = db['tasks']
    tasks: "list[Task]" = [Task(doc['task_name'], doc['owner'], doc['contributors'], doc['status'], \
                           doc['description'], doc['comments'], False) \
                           for doc in tasks_collection.find({})]
    return tasks

def clear_all_tasks() -> None:
    db = client['tasks_database']
    tasks_collection = db['tasks']
    tasks_collection.delete_many({})