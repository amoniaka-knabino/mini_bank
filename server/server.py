import json
from flask import Flask, jsonify, request
from Database import Database
import helpers.exceptions as e
import helpers.decorators as d
import time
import threading

app = Flask(__name__)
db = None

def hold_controller():
    while(True):
        if db is not None:
            time.sleep(60*10)
            print("Making everyones hold to zero")
            db.substract_hold_of_every_sub()
            

@app.before_first_request
def before_request():
    global db 
    db = Database()
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
    return jsonify(db.dump_users_to_dict_for_json())

@app.route('/api/status', methods=["POST"])
@d.need_args("uuid")
def user_from_json(uuid=None):
    global db
    addition = None
    try:
        addition = request.get_json()["addition"]
        addition = db.select_user_by_uuid(uuid).dict_for_json()
        return jsonify({"status":200, "result": True, "addition":addition})
    except Exception as exception:
        return e.handle_exception(exception, addition)


@app.route('/api/add', methods=["POST"])
@d.need_args("sum", "uuid")
def add(sum=None, uuid=None):
    global db
    addition = None
    try:
        addition = request.get_json()["addition"]
        user = db.select_user_by_uuid(uuid)
        user.add(sum)
        print(f"add {sum} to {user.uuid}, now balance is {user.balance}")
        db.update_balance(user)
        return jsonify({"status":200, "result": True})
    except Exception as exception:
        return e.handle_exception(exception, addition)


@app.route('/api/substract', methods=["POST"])
@d.need_args("sum", "uuid")
def substract(sum=None, uuid=None):
    global db
    addition = None
    try:
        addition = request.get_json()["addition"]
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
    db.drop_table()
    db.create_table()
    return jsonify({"status":200, "result": True})

@app.route('/api/load_db', methods=["POST"])
def load_db_from_json():
    global db
    addition = None
    try:
        posted_json = request.get_json()
        addition = posted_json["addition"]
        print(f"json from POST request: {posted_json}")
        db.load_from_json(posted_json)
        return jsonify({"status":200, "result": True})
    except Exception as exception:
        return e.handle_exception(exception, addition)
