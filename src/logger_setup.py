import logging
import pathlib
from pathlib import Path

#### Logging configuration : 


def setup_logging(file_path):
    '''creating a function for logging errors and info inside src/log_files/ folder'''
    
    file_name = Path(file_path).stem
    
    log_dir = Path('src/log_files')
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # log file path
    log_file = log_dir/f'{file_name}.log'
    
    # configure logger
    
    logger = logging.getLogger(file_name)
    logger.setLevel(logging.DEBUG) # Set level to DEBUG for main logger

    # setting Console Handler and File handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
# Add handlers to the logger
    if not logger.hasHandlers() : # To avoid adding multiple handlers if logger is called multiple times
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        
    return logger