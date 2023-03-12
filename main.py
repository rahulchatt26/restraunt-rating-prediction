from restaurant.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig
from restaurant.exception import RestaurantException
import sys, os
from restaurant.components.data_ingestion import DataIngestion

if __name__=="__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        data_ingestion = DataIngestion(data_ingesion_config=data_ingestion_config)
        data_ingestion.initiate_data_ingestion()
    except Exception as e:
        raise RestaurantException(e, sys)