import os

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi

CONNECTION_STRING = os.environ.get('CONNECTION_STRING')

client = AsyncIOMotorClient(CONNECTION_STRING, server_api=ServerApi("1"))

database_name = "development"
collection_name = "cameras"

database = client[database_name]
collection = database[collection_name]
