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
            try:
                posted_json = request.get_json()
                print(posted_json)
                kwargs = {}
                for key in needed_args_list:
                    kwargs[key] = posted_json["addition"][key]
                print(f"extract: {kwargs}")
                return func(**kwargs)
            except Exception as e:
                print(e)
        return inner

    return real_decorator
    