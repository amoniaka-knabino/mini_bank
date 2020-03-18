from flask import Flask, jsonify, request

class API_Exception(Exception):
    pass

class ClosedAccountException(API_Exception):
    pass

class UserNotFoundException(API_Exception):
    pass

def handle_exception(exception, addition):
    print(f"handle {type(exception)}")
    if type(exception) is UserNotFoundException:
        http_code = 404
        return jsonify({"status":http_code, "result": False,
                        "addition":addition,
                        "description": "User is not found in database"}), http_code
    else:
        http_code = 500
        return jsonify({"status":http_code, "result": False}), http_code
