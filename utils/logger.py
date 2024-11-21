import logging
import os
from datetime import datetime

LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
logs_path=os.path.join(os.getcwd(),"logs",LOG_FILE)
os.makedirs(logs_path, exist_ok=True)
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)


class Logging():
    logger = None
    def __init__(self):
        logging.basicConfig(filename=LOG_FILE_PATH,
                            format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
                            filemode='w',
                            level=logging.DEBUG)
        
        self.logger = logging.getLogger()

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)