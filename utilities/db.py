from abstractions.utility import IUtility


class DataBaseUtility(IUtility):

    def __init__(self, urn: str = None) -> None:
        super().__init__(urn)

    def connect(self):
        pass