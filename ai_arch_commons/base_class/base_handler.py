import logging
from abc import abstractmethod, ABC


class BaseHandler(ABC):
    def __init__(self):
        super(BaseHandler, self).__init__()
        logging.info("BaseHandler: initialized.")

    @abstractmethod
    def run(self):
        pass
