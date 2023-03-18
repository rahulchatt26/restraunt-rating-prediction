from restaurant.exception import RestaurantException
from restaurant.logger import logging
from restaurant.predictor import ModelResolver
import pandas as pd
import numpy as np
from restaurant.utils import load_object,converting_columns,drop_columns
import os,sys
from datetime import datetime
from typing import List
from restaurant.config import PREDICTOR_COLUMNS_LIST

PREDICTION_DIR="prediction"


def start_single_prediction(input:List)->float:
    try:
        logging.info(f"Creating model resolver object")
        model_resolver = ModelResolver(model_registry="saved_models")
        logging.info(f"Reading user input values :{input}")
        logging.info(f"creating dataframe")
        df = pd.DataFrame(data=input, columns=PREDICTOR_COLUMNS_LIST)
        logging.info(f"{df}")

        logging.info(f"Converting datatype for columns")
        df = converting_columns(df=df)

        #validation
        logging.info(f"Loading transformer to transform dataset")
        transformer = load_object(file_path=model_resolver.get_latest_transformer_path())
        
        input_feature_names =  list(transformer.feature_names_in_)
        logging.info(f"{input_feature_names}")
        input_arr = transformer.transform(df[input_feature_names])

        logging.info(f"Loading model to make prediction")
        model = load_object(file_path=model_resolver.get_latest_model_path())
        prediction = float(model.predict(input_arr))
        
        return prediction
    except Exception as e:
        raise RestaurantException(e, sys)