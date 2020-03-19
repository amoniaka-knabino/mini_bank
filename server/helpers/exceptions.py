from flask import jsonify
import json
import psycopg2


class API_Exception(Exception):
    pass


class ClosedAccountException(API_Exception):
    pass


class UserNotFoundException(API_Exception):
    pass


class InvalidSumException(API_Exception):
    pass


def handle_exception(exception, addition):
    print(f"handle {type(exception)}")
    if type(exception) is UserNotFoundException:
        http_code = 404
        return jsonify({"status": http_code, "result": False,
                        "addition": addition,
                        "description": "User is not found in database"}), http_code
    if type(exception) is InvalidSumException:
        http_code = 400
        return jsonify({"status": http_code, "result": False,
                        "addition": addition,
                        "description": "Sum param can't be negative"}), http_code
    if type(exception) is ClosedAccountException:
        http_code = 403
        return jsonify({"status": http_code, "result": False,
                        "addition": addition,
                        "description": "Can't execue operations with closed account"}), http_code
    if type(exception) is json.decoder.JSONDecodeError:
        http_code = 400
        return jsonify({"status": http_code, "result": False,
                        "addition": addition,
                        "description": "Bad JSON"}), http_code
    if type(exception) is psycopg2.errors.UniqueViolation:
        http_code = 400
        return jsonify({"status": http_code, "result": False,
                        "addition": addition,
                        "description": "Tried to add subscriber who are already exists in database"}), http_code
    else:
        print(exception)
        http_code = 500
        return jsonify({"status": http_code, "result": False}), http_code
