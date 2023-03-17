from restaurant.entity import artifact_entity,config_entity
from restaurant.exception import RestaurantException
from restaurant.logger import logging
from typing import Optional
import os,sys 
from restaurant import utils
from sklearn.metrics import r2_score
from sklearn.tree import DecisionTreeRegressor


class ModelTrainer:
    def __init__(self,model_trainer_config:config_entity.ModelTrainerConfig,
                data_transformation_artifact:artifact_entity.DataTransformationArtifact):
        try:
            logging.info(f"{'>>'*20} Model Trainer {'<<'*20}")
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e:
            raise RestaurantException(e, sys)


    def train_model(self,x,y):
        try:
            dt_reg = DecisionTreeRegressor(max_depth=6,criterion='squared_error')
            dt_reg.fit(x,y)
            return dt_reg
        except Exception as e:
            raise RestaurantException(e, sys)


    def initiate_model_trainer(self,)->artifact_entity.ModelTrainerArtifact:
        try:
            logging.info(f"Loading train and test array.")
            input_train_arr = utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_path)
            input_test_arr = utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_path)

            target_train_array = utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_col_path)
            target_test_array = utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_col_path)


            logging.info(f"Train the model")
            model = self.train_model(x=input_train_arr,y=target_train_array)

            logging.info(f"Calculating f1 train score")
            yhat_train = model.predict(input_train_arr)
            r2_train_score  =r2_score(y_true=target_train_array, y_pred=yhat_train)

            logging.info(f"Calculating f1 test score")
            yhat_test = model.predict(input_test_arr)
            r2_test_score  =r2_score(y_true=target_test_array, y_pred=yhat_test)
            
            logging.info(f"train score:{r2_train_score} and tests score {r2_test_score}")
            #check for overfitting or underfiiting or expected score
            logging.info(f"Checking if our model is underfitting or not")
            if r2_test_score<self.model_trainer_config.expected_score:
                raise Exception(f"Model is not good as it is not able to give \
                expected accuracy: {self.model_trainer_config.expected_score}: model actual score: {r2_test_score}")

            logging.info(f"Checking if our model is overfiiting or not")
            diff = abs(r2_train_score-r2_test_score)

            if diff>self.model_trainer_config.overfitting_threshold:
                raise Exception(f"Train and test score diff: {diff} is more than overfitting threshold {self.model_trainer_config.overfitting_threshold}")

            #save the trained model
            logging.info(f"Saving mode object")
            utils.save_object(file_path=self.model_trainer_config.model_path, obj=model)

            #prepare artifact
            logging.info(f"Prepare the artifact")
            model_trainer_artifact  = artifact_entity.ModelTrainerArtifact(model_path=self.model_trainer_config.model_path, 
            r2_train_score=r2_train_score, r2_test_score=r2_test_score)
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise RestaurantException(e, sys)