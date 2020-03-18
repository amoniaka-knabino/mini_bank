from functools import wraps
import helpers.exceptions as e

def check_status(func):
    @wraps(func)
    def checked(self, *args):
        if not self.status:
            raise e.ClosedAccountException()
        else:
            return func(self, *args)
    return checked