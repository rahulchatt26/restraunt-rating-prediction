import os, sys
from datetime import datetime
from restaurant.exception import RestaurantException
from restaurant.logger import logging

FILE_NAME = "restaurant.csv"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"

class TrainingPipelineConfig:
    def __init__(self):
        try:
            self.artifact_dir = os.path.join(os.getcwd(),"artifact",datetime.now().strftime('%m%d%Y__%H%M%S'))
        except Exception as e:
            raise RestaurantException(e, sys)
        

class DataIngestionConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        try:
            self.database_name = "food"
            self.collection_name = "restraunt"
            self.data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir, "data_ingestion")
            self.feature_store_file_path = os.path.join(self.data_ingestion_dir, "feature_store", FILE_NAME)
            self.train_file_path = os.path.join(self.data_ingestion_dir, "dataset", TRAIN_FILE_NAME)
            self.test_file_path = os.path.join(self.data_ingestion_dir, "dataset", TEST_FILE_NAME)
            self.test_size = 0.3
        except Exception as e:
            raise RestaurantException(e, sys)