class InvalidQueryException(Exception):
    def __init__(self, message):
        self.message = message


class InvalidQueryParamException(Exception):
    def __init__(self, message):
        self.message = message
