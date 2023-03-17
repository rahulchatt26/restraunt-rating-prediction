import pandas as pd
from restaurant.exception import RestaurantException
from restaurant.logger import logging
import os, sys
import yaml
import numpy as np
from restaurant.config import mongo_client
from restaurant.config import PREDICTOR_FLOAT_COLUMN,PREDICTOR_INT_CLOUMNS_LIST,REQUIRED_CLOUMNS_LIST,PREDICTOR_CATEGORICAL_COLUMNS_LIST
import dill


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
    
def drop_columns(df:pd.DataFrame)->pd.DataFrame:
    try:
        columns = df.columns
        for req_col in REQUIRED_CLOUMNS_LIST:
            if req_col not in columns:
                logging.info(f"Missing required column: {req_col}")
                raise RestaurantException(e, sys)
        df = df[REQUIRED_CLOUMNS_LIST]
        return df
    except Exception as e:
        raise RestaurantException(e, sys)
    
def converting_columns(df:pd.DataFrame)->pd.DataFrame:
    try:
        logging.info(f"converting datatype of columns: {PREDICTOR_FLOAT_COLUMN} as float")
        include_columns = [PREDICTOR_FLOAT_COLUMN]
        df = convert_columns_float(df=df, include_columns=include_columns)

        logging.info(f"converting datatype of columns: {PREDICTOR_INT_CLOUMNS_LIST} as int")
        include_columns = PREDICTOR_INT_CLOUMNS_LIST
        df = convert_columns_int(df=df, include_columns=include_columns)

        logging.info(f"encondig categorical columns: [{PREDICTOR_CATEGORICAL_COLUMNS_LIST}]")
        include_columns = PREDICTOR_CATEGORICAL_COLUMNS_LIST
        df = encode_categorical_columns(df=df, include_columns=include_columns)

        return df
        
    except Exception as e:
        raise RestaurantException(e, sys)
    
def convert_columns_float(df:pd.DataFrame,include_columns:list)->pd.DataFrame:
    try:
        for column in df.columns:
            if column in include_columns:
                df[column]=df[column].astype('float')
        return df
    except Exception as e:
        raise e
    

def convert_columns_int(df:pd.DataFrame,include_columns:list)->pd.DataFrame:
    try:
        for column in df.columns:
            if column in include_columns:
                df[column]=df[column].astype('int')
        return df
    except Exception as e:
        raise e

def encode_categorical_columns(df:pd.DataFrame,include_columns:list)->pd.DataFrame:
    try:
        for categorical_column in include_columns:
            logging.info(f"Encoding for column: {categorical_column}, Yes=1, No=0")
            df[categorical_column].replace({'Yes':1,'No':0},inplace=True)
        return df
    except Exception as e:
        raise RestaurantException(e, sys)

def write_yaml_file(file_path,data:dict):
    try:
        file_dir = os.path.dirname(file_path)
        os.makedirs(file_dir,exist_ok=True)
        with open(file_path,"w") as file_writer:
            yaml.dump(data,file_writer)
    except Exception as e:
        raise RestaurantException(e, sys)
    

def save_numpy_array_data(file_path: str, array: np.array):
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise RestaurantException(e, sys) from e

def load_numpy_array_data(file_path: str) -> np.array:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise RestaurantException(e, sys) from e
    

def save_object(file_path: str, obj: object) -> None:
    try:
        logging.info("Entered the save_object method of utils")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
        logging.info("Exited the save_object method of utils")
    except Exception as e:
        raise RestaurantException(e, sys) from e


def load_object(file_path: str, ) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} is not exists")
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise RestaurantException(e, sys) from e