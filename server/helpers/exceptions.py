class API_Exception(Exception):
    pass

class ClosedAccountException(API_Exception):
    pass

class UserNotFoundException(API_Exception):
    pass