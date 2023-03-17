from restaurant.exception import RestaurantException
from restaurant.pipeline.training_pipeline import start_training_pipeline
from restaurant.pipeline.batch_prediction import start_batch_prediction
import sys, os


if __name__=="__main__":
    try:
        # model_pusher_artifact = start_training_pipeline()
        # print(model_pusher_artifact)
        input_file_path = "F:\\End-to-End-ML-Project\\restraunt-rating-prediction\\ZomatoData.csv"
        prediction_path = start_batch_prediction(input_file_path=input_file_path)
        print(prediction_path)

    except Exception as e:
        raise RestaurantException(e, sys)