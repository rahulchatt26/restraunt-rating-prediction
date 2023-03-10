from dotenv import load_dotenv
import pandas as pd
import pymongo
import json
import os

print("Loading dotenv file...")
load_dotenv()


mongo_db_url:str = os.getenv("MONGO_DB_URL")
mongo_client:str = pymongo.MongoClient(mongo_db_url)

DATA_FILE_PATH:str = "F:\\End-to-End-ML-Project\\restraunt-rating-prediction\\ZomatoData.csv"
DATABASE_NAME:str = "food"
COLLECTION_NAME:str = "restraunt"


if __name__=="__main__":
    df = pd.read_csv(DATA_FILE_PATH,encoding='latin')
    print(f"ROWS: {df.shape[0]}, COLUMNS: {df.shape[1]}")

    #convert the dataframe to json so that we can dump the records into mongodb
    df.reset_index(drop=True, inplace=True)
    json_record = list(json.loads(df.T.to_json()).values())
    print(json_record[0])

    #insert converted json records into mongodb
    mongo_client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)