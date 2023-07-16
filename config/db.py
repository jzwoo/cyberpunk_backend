import os
from pip._vendor import certifi
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv('MONGO_URI'), tlsCAFile=certifi.where())

try:
    client.admin.command('ping')
    print('connected')
except Exception as e:
    print(e)
