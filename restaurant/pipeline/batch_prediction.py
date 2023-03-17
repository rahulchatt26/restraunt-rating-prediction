from restaurant.exception import RestaurantException
from restaurant.logger import logging
from restaurant.predictor import ModelResolver
import pandas as pd
import numpy as np
from restaurant.utils import load_object,converting_columns,drop_columns
import os,sys
from datetime import datetime

PREDICTION_DIR="prediction"


def start_batch_prediction(input_file_path):
    try:
        os.makedirs(PREDICTION_DIR,exist_ok=True)
        logging.info(f"Creating model resolver object")
        model_resolver = ModelResolver(model_registry="saved_models")
        logging.info(f"Reading file :{input_file_path}")
        df = pd.read_csv(input_file_path,encoding='latin')

        #remove unwanted columns and convert datatypes
        logging.info("Removing unwanted columns from the dataset")
        df = drop_columns(df=df)

        logging.info(f"Converting datatype for columns")
        df = converting_columns(df=df)

        #validation
        logging.info(f"Loading transformer to transform dataset")
        transformer = load_object(file_path=model_resolver.get_latest_transformer_path())
        
        input_feature_names =  list(transformer.feature_names_in_)
        input_arr = transformer.transform(df[input_feature_names])

        logging.info(f"Loading model to make prediction")
        model = load_object(file_path=model_resolver.get_latest_model_path())
        prediction = model.predict(input_arr)
        
        df["prediction"]=prediction

        prediction_file_name = os.path.basename(input_file_path).replace(".csv",f"_{datetime.now().strftime('%m%d%Y__%H%M%S')}.csv")
        prediction_file_path = os.path.join(PREDICTION_DIR,prediction_file_name)
        df.to_csv(prediction_file_path,index=False,header=True)
        return prediction_file_path
    except Exception as e:
        raise RestaurantException(e, sys)