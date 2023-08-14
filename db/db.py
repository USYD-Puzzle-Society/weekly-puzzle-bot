import pymongo
import os
import sys
from dotenv import load_dotenv

from classes.Task import Task

load_dotenv()

uri = f"mongodb+srv://{os.getenv['DB_USER']}:{os.getenv['DB_PASSWORD']}@dev.cpp759d.mongodb.net/?retryWrites=true&w=majority"

try:
    client = pymongo.MongoClient(uri)
except pymongo.errors.ConfigurationError:
    print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
    sys.exit(1)

async def create_task(task: Task) -> None:
    db = client['tasks_database']
    tasks_collection = db['tasks']
    tasks_collection.insert_one(task.to_dict())

async def get_tasks() -> 'list[Task]':
    db = client['tasks_database']
    tasks_collection = db['tasks']
    tasks: "list[Task]" = [Task(doc['task_name'], doc['owner'], doc['contributors'], doc['status'], \
                           doc['description'], doc['comments'], False) \
                           for doc in tasks_collection]
    return tasks