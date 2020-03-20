from functools import wraps
import json
from flask import Flask, jsonify, request
import helpers.exceptions as e
import werkzeug

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
            print("in needed args")
            try:
                posted_json = request.get_json()
            except werkzeug.exceptions.BadRequest:
                raise e.JSONObjectExpected
            print(f"posted json: {posted_json}")
            kwargs = {}
            for key in needed_args_list:
                try:
                    if key == 'addition':
                        kwargs[key] = posted_json[key]
                    else:
                        kwargs[key] = posted_json["addition"][key]
                except KeyError:
                    raise e.SomeOtherArgsRequired
            print(f"extracted: {kwargs}")
            return func(**kwargs)
        return inner
    return real_decorator

def safe_run(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        print("in safe run")
        try:
           return func(*args, **kwargs)

        except Exception as exc:
            print(exc, args, kwargs)
            return e.handle_exception(exc, None)

    return func_wrapper



