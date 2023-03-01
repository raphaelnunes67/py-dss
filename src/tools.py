import logging
import logging.handlers
import os
import sys
from pathlib import Path


class Log:
    dir_path = Path(os.path.dirname(__file__) + "/../logs")

    def __init__(self, logs_path=dir_path):
        self.logger = None
        self.logs_path = Path(logs_path)
        if not os.path.exists(self.logs_path):
            os.makedirs(self.logs_path, exist_ok=True)

    def set_logger_stdout(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

        return self.logger

    def set_logger_file(self, logger_name):
        self.logger = logging.getLogger(logger_name)
        path = Path(self.logs_path, logger_name + '.log')
        file_handler = logging.handlers.RotatingFileHandler(filename=str(path),
                                                            mode='a',
                                                            maxBytes=10000000,
                                                            backupCount=10)
        formatter = logging.Formatter('[ %(asctime)s ] %(levelname)s %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.logger.setLevel(logging.DEBUG)

        return self.logger
