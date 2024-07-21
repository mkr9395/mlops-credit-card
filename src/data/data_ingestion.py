import pandas as pd
import numpy as np
from pathlib import Path


import yaml
import logging

from sklearn.model_selection import train_test_split


from src.logger_setup import setup_logging
logger = setup_logging(__file__)


def load_params(params_path:str)-> tuple:
    '''load params from params.yaml file'''
    
    try:
        with open(params_path,'r') as params_file:
            params = yaml.safe_load(params_file)
            
        test_size = params['data_ingestion']['test_size']
        random_state = params['data_ingestion']['random_state']
        data_path = params['data_ingestion']['data_path']
        save_path = params['data_ingestion']['save_path']
        
        logger.info(f'test_size and random_state fetched from {params_path}')
        return data_path, save_path , test_size, random_state
    except FileNotFoundError as e:
        logger.error('file not found at %s: %s', params_path, e )
        raise
    except yaml.YAMLError as e:
        logger.error('Yaml error %s',e)
        raise
    except Exception as e:
        logger.error('Unexpected error while reading the file %s',e)
        raise
    
        
        
def read_data(data_path:str)-> pd.DataFrame:
    '''reading data from data/external/'''
    
    try:        
        df = pd.read_csv(data_path)
        logger.info(f'data read from {data_path}')
        return df
    
    except FileNotFoundError as e:
        logger.error('Data file not found at %s: %s', data_path, e)
        raise
    except pd.errors.ParserError as e:
        logger.error('Failed to parse the CSV file: %s', e)
        raise
    except Exception as e:
        logger.error('Unexpected error while reading the data at %s ',e)
        raise
    
    
def data_split(df:pd.DataFrame, test_size:float, random_state:int) -> tuple[pd.DataFrame, pd.DataFrame]:
    ''''split data into train and test'''
    try:
        train_data,test_data = train_test_split(df,test_size=test_size,random_state=random_state)
        logger.info('raw data splitted into train and test_data')
        return train_data,test_data
    except Exception as e:
        logger.error('Error occurred while splitting data: %s', e)
        raise
    
def save_data(train_data:pd.DataFrame,test_data:pd.DataFrame,save_file_path:str)-> str:
    '''saving train_data and test_data into data/raw folder'''
    try :
        save_file_path = Path(save_file_path)
        
        # create folder if already not present:
        save_file_path.mkdir(parents=True, exist_ok=True)
        
        train_data.to_csv(save_file_path/'train.csv',index=False)
        test_data.to_csv(save_file_path/'test.csv',index=False)
        logger.info(f'train and test data saved at {save_file_path}')
        return 'Data Ingestion completed successfully'
    
    except Exception as e:
        logger.error('Unexpected error occurred: %s', e)
        raise
        
    
    
def main():
    try:
        params_file_path = Path('params.yaml')
        
        data_path, save_path, test_size, random_state = load_params(params_file_path)
        
        df = read_data(data_path)
        
        train_data, test_data = data_split(df, test_size=test_size, random_state=random_state)
        
        save_data(train_data,test_data,save_path)
        
        logger.info(f'size of train :  ({train_data.shape}) and test : ({test_data.shape})')
    except Exception as e:
        logger.error('Error occurred in main function: %s', e)
        
if __name__ == '__main__':
    main()
    
    






