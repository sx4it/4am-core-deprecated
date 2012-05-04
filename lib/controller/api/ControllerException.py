'''
Controller defined exception
'''

class InternalError(Exception):
    '''
    Exception raised for critical error in the controller
    '''
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class InvalidAgumentError(Exception):
    '''
    Exception raised for invalid argument given to the controller
    '''
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class MissingArgumentError(Exception):
    '''
    Exception raised for missing argument given to the controller
    '''
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr("Missing value: " + self.value)

class AccessForbiddenError(Exception):
    '''
    Raised when a user attempts a forbidden action
    '''
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
