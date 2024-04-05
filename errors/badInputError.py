from abstractions.error import IError


class BadInputError(Exception, IError):

    def __init__(self, response_message: str, response_key: dict, status_code: int) -> None:
        super().__init__()
        IError.__init__(self)

        self.response_message = response_message
        self.response_key = response_key
        self.status_code = status_code
