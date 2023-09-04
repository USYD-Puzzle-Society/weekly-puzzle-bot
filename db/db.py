import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from beanie import init_beanie

from classes.SubcomTask import Task, TaskMetadata

load_dotenv()

uri = os.getenv('DB_URI')

async def init_db():
    client = AsyncIOMotorClient(uri, server_api=ServerApi('1'))
    await init_beanie(client['tasks_database'], document_models=[Task, TaskMetadata])
