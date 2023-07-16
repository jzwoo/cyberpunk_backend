from typing import Mapping, Any
from pymongo.database import Database


def get_users_controller(db: Database[Mapping[str, Any]]):
    users = db['users'].find()
    return users
