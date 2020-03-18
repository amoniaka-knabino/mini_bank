from functools import wraps
import json
from flask import Flask, jsonify, request
import helpers.exceptions as e

def check_status(func):
    @wraps(func)
    def checked(self, *args):
        if not self.status:
            raise e.ClosedAccountException()
        else:
            return func(self, *args)
    return checked

def need_args(*needed_args_list):
    def real_decorator(func):
        @wraps(func)
        def inner(*args, **kws):
            posted_json = request.get_json()
            print(f"posted json: {posted_json}")
            kwargs = {}
            for key in needed_args_list:
                if key == 'addition':
                    kwargs[key] = posted_json[key]
                else:
                    kwargs[key] = posted_json["addition"][key]
            print(f"extracted: {kwargs}")
            return func(**kwargs)
        return inner
    return real_decorator
    