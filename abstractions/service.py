from abc import ABC
from loguru import logger

class IService(ABC):

    def __init__(self, urn: str = None) -> None:
        self.urn = urn
        self.logger = logger