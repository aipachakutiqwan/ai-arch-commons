import importlib
import logging
import os

from ai_arch_commons.log_management.config import get_app_config_parameters
from ai_arch_commons.log_management.log_management import configure_logger


class AIApp:
    def __init__(self):
        self.config_file = None
        self.log_config_file = None
        self.config = None
        self.service_obj = None

    def get_app_config_params(self):
        return get_app_config_parameters(self.config_file)

    def config_logger(self):
        configure_logger(self.log_config_file)

    def setup_config_and_log(self):
        self.config_file = os.getenv('APP_CONFIG_FILE')
        self.log_config_file = os.getenv('LOG_CONFIG_FILE')
        self.config = self.get_app_config_params()
        self.config_logger()
        logging.info("Config is read and logging lib is initialized.")

    def get_service_obj(self, service_module):
        return getattr(service_module, self.config["service_class"])()

    def setup_service_obj(self):
        module_path = self.config["service_module_path"]
        service_module = importlib.import_module(module_path)
        logging.info(f"Module at path={module_path} is loaded.")
        self.service_obj = self.get_service_obj(service_module)
        self.service_obj.setup_from_config(self.config["service_config"])
        logging.info(f"Module at path={module_path} is initialized.")

    def run_service(self):
        if self.service_obj is None:
            raise RuntimeError(f"Service at: module path={self.config['service_module_path']} is None.")
        self.service_obj.run_service()
