

class WMRevolutionError(Exception):
    pass


class BadRequestError(WMRevolutionError):

    """
    Error raised when a bad status code 
    is returned from a url request
    """

    def __init__(self, message):
        WMRevolutionError.__init__(self, message)
