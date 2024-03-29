from restaurant.predictor import ModelResolver
from restaurant.entity import config_entity,artifact_entity
from restaurant.exception import RestaurantException
from restaurant.logger import logging
from restaurant.utils import load_object
from sklearn.metrics import r2_score
import pandas  as pd
import sys,os
from restaurant.config import TARGET_COLUMN,PREDICTOR_FLOAT_COLUMN,PREDICTOR_INT_CLOUMNS_LIST,PREDICTOR_CATEGORICAL_COLUMNS_LIST
from restaurant.utils import convert_columns_float,convert_columns_int,encode_categorical_columns


class ModelEvaluation:
    def __init__(self,
        model_eval_config:config_entity.ModelEvaluationConfig,
        data_ingestion_artifact:artifact_entity.DataIngestionArtifact,
        data_transformation_artifact:artifact_entity.DataTransformationArtifact,
        model_trainer_artifact:artifact_entity.ModelTrainerArtifact      
        ):
        try:
            logging.info(f"{'>>'*20}  Model Evaluation {'<<'*20}")
            self.model_eval_config=model_eval_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_transformation_artifact=data_transformation_artifact
            self.model_trainer_artifact=model_trainer_artifact
            self.model_resolver = ModelResolver()
        except Exception as e:
            raise RestaurantException(e,sys)



    def initiate_model_evaluation(self)->artifact_entity.ModelEvaluationArtifact:
        try:
            #if saved model folder has model then we will compare 
            #which model is best trained of the model from saved model folder

            logging.info("if saved model folder has model then we will compare "
            "which model is best trained of the model from saved model folder")
            latest_dir_path = self.model_resolver.get_latest_dir_path()
            if latest_dir_path==None:
                model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True,
                improved_accuracy=None)
                logging.info(f"Model evaluation artifact: {model_eval_artifact}")
                return model_eval_artifact

            #Finding location of transformer and model
            logging.info("Finding location of transformer and model")
            transformer_path = self.model_resolver.get_latest_transformer_path()
            model_path = self.model_resolver.get_latest_model_path()

            logging.info("Previous trained objects of transformer and model")
            #Previous trained  objects
            transformer = load_object(file_path=transformer_path)
            model = load_object(file_path=model_path)
            

            logging.info("Currently trained model objects")
            #Currently trained model objects
            current_transformer = load_object(file_path=self.data_transformation_artifact.transform_object_path)
            current_model  = load_object(file_path=self.model_trainer_artifact.model_path)
            
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            y_true = test_df[TARGET_COLUMN]

            # accuracy using previous trained model
            input_feature_name = list(transformer.feature_names_in_)
            print(input_feature_name)
            logging.info(f"x_true = {input_feature_name}")
            input_arr =transformer.transform(test_df[input_feature_name])
            y_pred = model.predict(input_arr)
            print(f"Prediction using previous model: {y_pred}")
            previous_model_score = r2_score(y_true=y_true, y_pred=y_pred)
            logging.info(f"Accuracy using previous trained model: {previous_model_score}")
           
            # accuracy using current trained model
            input_feature_name = list(current_transformer.feature_names_in_)
            input_arr =current_transformer.transform(test_df[input_feature_name])
            y_pred = current_model.predict(input_arr)
            y_true = test_df[TARGET_COLUMN]
            print(f"Prediction using trained model: {y_true}")
            current_model_score = r2_score(y_true=y_true, y_pred=y_pred)
            logging.info(f"Accuracy using current trained model: {current_model_score}")
            if current_model_score<=previous_model_score:
                logging.info(f"Current trained model is not better than previous model")
                raise Exception("Current trained model is not better than previous model")

            model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True,
            improved_accuracy=current_model_score-previous_model_score)
            logging.info(f"Model eval artifact: {model_eval_artifact}")
            return model_eval_artifact
        except Exception as e:
            raise RestaurantException(e,sys)
