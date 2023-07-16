import os
from dotenv import load_dotenv
from typing import Mapping, Any
from pymongo.database import Database

load_dotenv()


def get_users_controller(db: Database[Mapping[str, Any]]):
    users = db[os.getenv('MONGO_DATABASE_USERS_COLLECTION')].find()
    return users
