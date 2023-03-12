from dataclasses import dataclass
from pymongo import MongoClient
import os, sys

@dataclass
class EnvironmentVariable:
    mongo_db_url:str = os.getenv("MONGO_DB_URL")


env_var = EnvironmentVariable()
mongo_client = MongoClient(env_var.mongo_db_url)
