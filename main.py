import glob
import logging
import os
import shutil
import time
from pathlib import Path


def creating_logger(name, log_file, level=logging.DEBUG):
    # Specify the formate for the logging file
    file_formate = logging.Formatter(
        '{"time":"%(asctime)s", "name": "%(name)s","level": "%(levelname)s", "message": "%(message)s", "ThreadID": '
        '"%(thread)d", "ThreadName": "%(threadName)s"} '
    )
    # Create a file handler
    handler = logging.FileHandler(log_file, mode='a+')
    handler.setFormatter(file_formate)  # Set the format for the file
    logger = logging.getLogger(name)  # Create logger object
    logger.setLevel(level)  # Set the level (DEBUG is the default)
    logger.addHandler(handler)  # Add the handler
    return logger  # Retrun the logger object


"""
check new transactions function 
    search for new transactions 
    define the destination
    copy each transaction file to medvertex file in EDI_Connection/medvertex for processing  
    move the transaction file to sent directory 
"""


def check_new_transactions():
    try:
        new_transactions = glob.glob(pathname='../EDI_837/EDI_Transaction837/outbound/*.837')
        non_critical.info('Search for all new transactions files inside the outbound folder')
        Path("../EDI_Connection/request").mkdir(parents=True, exist_ok=True)
        destination = '../EDI_Connection/request'
        for transaction in new_transactions:
            shutil.copy(transaction, destination)
            shutil.move(transaction, 'sent')
    except FileExistsError:
        critical.error('Error in finding the claim files')
        print(FileExistsError, "from check new claims function")


"""
Main Method 
    create directory named sent 
    create logging directory if not exists
    call method check new transactions each 10 seconds checking for new transactions 
"""
if __name__ == '__main__':
    Path("sent").mkdir(parents=True, exist_ok=True)
    if not os.path.exists('./logging'):
        try:
            os.mkdir('./logging')
        except OSError:
            print("Creating the logging folder is falid")

    critical = creating_logger('critical', './logging/critical.log')
    non_critical = creating_logger('non_critical', './logging/non_critical.log')
    print("Start Working")
    while True:
        time.sleep(10)
        check_new_transactions()
