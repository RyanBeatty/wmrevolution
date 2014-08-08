


class WMRevolutionError(Exception):
	pass
    # def __str__(self):
    #     return "%s(%s)" % (self.__class__.__name__, self.args)


class BadRequestError(WMRevolutionError):
    """
    Error raised when a bad status code 
    is returned from a url request
    """
    def __init__(self, message):
    	WMRevolutionError.__init__(self, message)


