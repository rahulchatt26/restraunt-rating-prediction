import pandas as pd
from restaurant.exception import RestaurantException
from restaurant.logger import logging
import os, sys
from restaurant.config import mongo_client


def get_collection_as_dataframe(database_name:str, collection_name:str)->pd.DataFrame:
    try:
        """
        Description: This function returns colection as DataFrame
        =========================================================
        Params:
        database_name: database name
        collection_name: collection name
        =========================================================
        return Pandas dataframe of a collection
        """
        logging.info(f"Reading data from database: {database_name} collection: {collection_name}")
        df = pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        logging.info(f"Found columns: {df.columns}")

        if "_id" in df.columns:
            logging.info(f"Dropping column: _id ")
            df = df.drop("_id",axis=1)
        logging.info(f"Row and columns in df: {df.shape}")
        return df

    except Exception as e:
        raise RestaurantException(e, sys)