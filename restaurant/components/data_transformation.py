from restaurant.entity import config_entity, artifact_entity
from restaurant.logger import logging
from restaurant.exception import RestaurantException
import os,sys
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
from restaurant.config import TARGET_COLUMN
from restaurant import utils
from restaurant.utils import convert_columns_float,write_yaml_file,convert_columns_int,encode_categorical_columns
from restaurant.config import TARGET_COLUMN,PREDICTOR_FLOAT_COLUMN,PREDICTOR_INT_CLOUMNS_LIST,PREDICTOR_CATEGORICAL_COLUMNS_LIST

class DataTransformation:
    def __init__(
            self,
            data_ingestion_artifact:artifact_entity.DataIngestionArtifact,
            data_transformation_config:config_entity.DataTransformationConfig):
        try:
            logging.info(f"{'>>'*20} Data Transformation {'<<'*20}")
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise RestaurantException(e, sys)
        
    @classmethod
    def get_data_transformer_object(cls)->Pipeline:
        try:
            min_max_scaler = MinMaxScaler()
            pipeline = Pipeline(steps=[
                    ('MinMaxNormalization',min_max_scaler)
                ])
            return pipeline
        except Exception as e:
            raise RestaurantException(e, sys)


    def initiate_data_transformation(self,) -> artifact_entity.DataTransformationArtifact:
        try:
            #reading training and testing file
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            
            #selecting input feature for train and test dataframe
            logging.info(f"df columns ===> {train_df.columns}")
            input_feature_train_df=train_df.drop(TARGET_COLUMN,axis=1)
            input_feature_test_df=test_df.drop(TARGET_COLUMN,axis=1)
            logging.info(f"df columns ===> {input_feature_train_df.columns}")

            #selecting target feature for train and test dataframe
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_test_df = test_df[TARGET_COLUMN]

            #converting target column from dataframe to ndarray
            target_feature_train_array = target_feature_train_df.to_numpy()
            target_feature_test_array = target_feature_test_df.to_numpy()

            transformation_pipleine = DataTransformation.get_data_transformer_object()
            transformation_pipleine.fit(input_feature_train_df)

            #transforming input features
            logging.info(f"Normalise input freatures for Train & Test dataframe")
            input_feature_train_arr = transformation_pipleine.transform(input_feature_train_df)
            input_feature_test_arr = transformation_pipleine.transform(input_feature_test_df)


            #save numpy array
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_path,
                                        array=input_feature_train_arr)
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_path,
                                        array=input_feature_test_arr)
            
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_col_path,
                                        array=target_feature_train_array)
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_col_path,
                                        array=target_feature_test_array)
            
            utils.save_object(file_path=self.data_transformation_config.transform_object_path,
                              obj=transformation_pipleine)

            data_transformation_artifact = artifact_entity.DataTransformationArtifact(
                transform_object_path=self.data_transformation_config.transform_object_path,
                transformed_train_path = self.data_transformation_config.transformed_train_path,
                transformed_test_path = self.data_transformation_config.transformed_test_path,
                transformed_train_col_path=self.data_transformation_config.transformed_train_col_path,
                transformed_test_col_path=self.data_transformation_config.transformed_test_col_path
            )

            logging.info(f"Data transformation object {data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise RestaurantException(e, sys)