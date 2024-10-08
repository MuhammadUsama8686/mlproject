from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
import os 
import sys
from src.components.data_transformation import Data_Transformation, data_transformation_config
from src.components.model_trainer import ModelTrainer
from src.components.model_trainer import ModelTrainerConfig


@dataclass
class DataIngestionConfig():
    train_data_path : str = os.path.join('artifacts', 'train.csv')
    test_data_path : str = os.path.join('artifacts', 'test.csv')
    raw_data_path : str = os.path.join('artifacts', 'data.csv')



class DataIngestion():
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initialize_data_ingestion(self):
        logging.info('Initializing Ingestion')
        try:
            df = pd.read_csv('notebook\data\StudentsPerformance.csv')
            logging.info('Data loaded successfully')
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path, index=False)
            logging.info('Raw data saved successfully')

            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True) 
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info('Data split and saved successfully')

            return (self.ingestion_config.train_data_path, self.ingestion_config.test_data_path)


        except Exception as e:
            raise CustomException(sys, e)


if __name__ == '__main__':
    obj = DataIngestion()
    train_data,test_data=obj.initialize_data_ingestion()

    data_transformation=Data_Transformation()
    train_arr,test_arr,_=data_transformation.initiate_data_transformation(train_data,test_data)
   
    modeltrainer=ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_arr,test_arr))