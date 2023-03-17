from dataclasses import dataclass
from pymongo import MongoClient
import os, sys

@dataclass
class EnvironmentVariable:
    mongo_db_url:str = os.getenv("MONGO_DB_URL")


env_var = EnvironmentVariable()
mongo_client = MongoClient(env_var.mongo_db_url)

TARGET_COLUMN = "Rating"
PREDICTOR_FLOAT_COLUMN = "Average Cost for two"
PREDICTOR_INT_CLOUMNS_LIST = ["Votes", "Price range"]
PREDICTOR_CATEGORICAL_COLUMNS_LIST = ['Has Table booking','Has Online delivery']
REQUIRED_CLOUMNS_LIST = ['Votes','Average Cost for two','Has Table booking','Has Online delivery','Price range','Rating']
