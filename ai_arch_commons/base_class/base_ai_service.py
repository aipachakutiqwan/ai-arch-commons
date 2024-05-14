import logging
from abc import ABC, abstractmethod
from typing import Dict


class BaseAIService(ABC):
    def __init__(self):
        logging.info("BaseAIService: initialized.")

    @abstractmethod
    def setup_from_config(self, config: Dict):
        pass

    @abstractmethod
    def run_service(self):
        pass
