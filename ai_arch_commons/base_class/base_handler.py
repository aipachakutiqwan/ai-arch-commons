import logging
from abc import abstractmethod, ABC


class BaseHandler(ABC):
    def __init__(self):
        logging.info("BaseHandler: initialized.")

    @abstractmethod
    def run(self):
        pass
