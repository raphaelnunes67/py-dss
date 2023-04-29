import logging
import logging.handlers
import os
import sys
from pathlib import Path
from typing import Union


class Log:
    dir_path = Path(os.path.dirname(__file__) + "/../logs")

    def __init__(self, logs_path=dir_path):
        self.logger = ''
        self.target_folder_path = None
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


class HandleFiles:

    def __init__(self):
        self.target_folder_path = None
        self.new_results_folder_path = None
        self.file_path = os.path.dirname(__file__)
        self.results_path = self.file_path + '/../results/'
        if not os.path.exists(Path(self.results_path)):
            os.mkdir(Path(self.results_path))

    def get_target_file_path(self, folder, file) -> Union[str, bool]:

        if os.path.exists(Path(self.file_path + '/../dss/' + folder + '/' + file)):
            self.target_folder_path = self.file_path + '/../dss/' + folder
            return str(Path(self.target_folder_path + '/' + file))
        return False

    def get_target_folder_path(self) -> str:

        return str(Path(self.target_folder_path))

    def set_folder_in_results(self, new_folder: str) -> None:
        self.new_results_folder_path = self.results_path + new_folder

        if os.path.exists(Path(self.new_results_folder_path)):
            return

        os.mkdir(Path(self.results_path + new_folder))

    def get_folder_path_in_results(self) -> str:
        return str(Path(self.new_results_folder_path))

    def remove_results_folder_content(self) -> None:

        files = os.listdir(self.new_results_folder_path)

        for file in files:
            file_path = os.path.join(self.new_results_folder_path, file)
            os.remove(file_path)

    def remove_file(self, file_name: str) -> bool:
        try:
            os.remove(Path(self.new_results_folder_path + '/' + file_name))
            return True
        except FileNotFoundError:
            return False

    def remove_folder(self) -> bool:
        try:
            os.rmdir(Path(self.new_results_folder_path))
            return True
        except FileNotFoundError:
            return False
