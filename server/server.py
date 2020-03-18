import json
from flask import Flask, jsonify, request
from Database import DatabaseClient
import helpers.exceptions as e
import helpers.decorators as d
import time
import threading

app = Flask(__name__)
def hold_controller():
    while(True):
        with DatabaseClient() as db:
            time.sleep(60*10)
            print("Making everyones hold to zero")
            db.substract_hold_of_every_sub()
            

@app.before_first_request
def before_request():
    thread = threading.Thread(target=hold_controller)
    thread.start()

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/ping')
def ping():
    return jsonify({'status':200})

@app.route('/api/subs')
def users():
    with DatabaseClient() as db:
        return jsonify({"addition": db.dump_users_to_dict_for_json()})

@app.route('/api/status', methods=["POST"])
@d.need_args("uuid", "addition")
def user_from_json(uuid=None, addition=None):
    try:
        with DatabaseClient() as db:
            addition = db.select_user_by_uuid(uuid).dict_for_json()
            return jsonify({"status":200, "result": True, "addition":addition})
    except Exception as exception:
        return e.handle_exception(exception, addition)


@app.route('/api/add', methods=["POST"])
@d.need_args("sum", "uuid", "addition")
def add(sum=None, uuid=None, addition=None):
    try:
        with DatabaseClient() as db:
            user = db.select_user_by_uuid(uuid)
            user.add(sum)
            print(f"add {sum} to {user.uuid}, now balance is {user.balance}")
            db.update_balance(user)
            return jsonify({"status":200, "result": True})
    except Exception as exception:
        return e.handle_exception(exception, addition)


@app.route('/api/substract', methods=["POST"])
@d.need_args("sum", "uuid", "addition")
def substract(sum=None, uuid=None, addition=None):
    try:
        with DatabaseClient() as db:
            print(f"extracted params is : {(sum, uuid)}")
            user = db.select_user_by_uuid(uuid)
            user.substract(sum)
            print(f"sub {sum} from {user.uuid}, now hold is {user.hold}")
            db.update_hold(user)
            return jsonify({"status":200, "result": True})
    except Exception as exception:
        return e.handle_exception(exception, addition)


@app.route('/api/refresh')
def refresh_db():
    with DatabaseClient() as db:
        db.drop_table()
        db.create_table()
        return jsonify({"status":200, "result": True})

@app.route('/api/load_db', methods=["POST"])
@d.need_args("addition")
def load_db_from_json(addition=None):
    try:
        with DatabaseClient() as db:
            print(f"json['addition'] from POST request: {addition}")
            db.load_from_json(addition)
            return jsonify({"status":200, "result": True, "addition":addition})
    except Exception as exception:
        return e.handle_exception(exception, addition)
