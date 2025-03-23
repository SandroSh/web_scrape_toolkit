import logging
import os
from datetime import datetime



def setup_logger(name:str, log_file: str = 'scraper.log') -> logging.Logger:
    """ 
        Configure and return a logger instance 
    """
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    os.makedirs('logs', exist_ok=True)
    log_path = os.path.join("logs",log_file)
    
    fh = logging.FileHandler(log_path)
    fh.setLevel(logging.INFO)
    
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    
    #Formatter
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s -%(levelname)s %(message)s'
    )
    
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger
    