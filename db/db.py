import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi

load_dotenv()

uri = os.getenv('DB_URI')

class Database():
    def __init__(self, uri):
        self.client = AsyncIOMotorClient(uri, server_api=ServerApi('1'))
        self.task_db = self.client['tasks_database']
        self.task_id_counter_collection = self.task_db['id_counter']
        self.tasks_collection = self.task_db['tasks']


database = Database(uri)