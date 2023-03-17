from restaurant.entity.config_entity import DataIngestionConfig
from restaurant.entity.artifact_entity import DataIngestionArtifact
from restaurant.exception import RestaurantException
from restaurant.logger import logging
import os, sys
from restaurant.utils import get_collection_as_dataframe, drop_columns, converting_columns
import pandas as pd
from sklearn.model_selection import train_test_split
class DataIngestion:
    def __init__(self, data_ingesion_config:DataIngestionConfig):
        try:
            logging.info(f"{'<<'*20} Data Ingestion {'>>'*20}")
            self.data_ingestion_config = data_ingesion_config
        except Exception as e:
            raise RestaurantException(e, sys)
        
    def initiate_data_ingestion(self)->DataIngestionArtifact:
        try:
            logging.info(f"Exporting collection data as pandas dataframe")
            #Exporting collection data as pandas dataframe
            df:pd.DataFrame = get_collection_as_dataframe(
                database_name=self.data_ingestion_config.database_name,
                collection_name = self.data_ingestion_config.collection_name)
            logging.info("Removing unwanted columns from the dataset")
            df = drop_columns(df=df)

            logging.info(f"Converting datatype for columns")
            df = converting_columns(df=df)

            logging.info("Save data in feature store")
            #Save data in feature store
            logging.info("Create feature store folder if not available")
            #Create feature store folder if not available
            feature_store_dir = os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(feature_store_dir,exist_ok=True)
            logging.info("Save df to feature store folder")
            #Save df to feature store folder
            df.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path, header=True, index=False)


            logging.info("split dataset into train and test set")
            #split dataset into train and test set
            train_df, test_df = train_test_split(df, test_size=self.data_ingestion_config.test_size,random_state=10)

            logging.info("create dataset directory folder if not available")
            #create dataset directory folder if not available
            dataset_dir = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dataset_dir, exist_ok=True)

            logging.info("Save train_df and test_df to dataset folder")
            #Save df to dataset folder
            logging.info(f"train_df shape: {train_df.shape}")
            train_df.to_csv(path_or_buf=self.data_ingestion_config.train_file_path, header=True, index=False)
            logging.info(f"test_df shape: {test_df.shape}")
            test_df.to_csv(path_or_buf=self.data_ingestion_config.test_file_path, header=True, index=False)

            #Prepare artifact
            data_ingestion_artifact = DataIngestionArtifact(
                feature_store_file_path=self.data_ingestion_config.feature_store_file_path,
                train_file_path=self.data_ingestion_config.train_file_path,
                test_file_path=self.data_ingestion_config.test_file_path
            )
            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise RestaurantException(e, sys)
