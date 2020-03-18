import json
from flask import Flask, jsonify, request
from Database import Database
import helpers.exceptions as e
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
def user_from_json():
    global db
    try:
        posted_json = request.get_json()
        print(posted_json)
        uuid = posted_json["addition"]["uuid"]
    except:
        http_code = 400
        return jsonify({"status":http_code, "result": False}), http_code
    try:
        addition = db.select_user_by_uuid(uuid).dict_for_json()
        return jsonify({"status":200, "result": True, "addition":addition})
    except e.UserNotFoundException:
        http_code = 404
        return jsonify({"status":http_code, "result": False,
                        "addition":{"uuid":uuid},
                        "description": "User is not found in database"}), http_code
    except:
        http_code = 500
        return jsonify({"status":http_code, "result": False}), http_code

@app.route('/api/add', methods=["POST"])
def add():
    global db
    try:
        posted_json = request.get_json()
        print(posted_json)
        addition = posted_json["addition"]
        uuid = addition["uuid"]
        summ = addition["sum"]
    except:
        http_code = 400
        return jsonify({"status":http_code, "result": False}), http_code
    try:
        user = db.select_user_by_uuid(uuid)
        user.add(summ)
        print(f"add {summ} to {user.uuid}, now balance is {user.balance}")
        db.update_balance(user)
        return jsonify({"status":200, "result": True, "addition":addition})
    except e.UserNotFoundException:
        http_code = 404
        return jsonify({"status":http_code, "result": False,
                        "addition":{"uuid":uuid},
                        "description": "User is not found in database"}), http_code
    except:
        http_code = 500
        return jsonify({"status":http_code, "result": False}), http_code

@app.route('/api/substract', methods=["POST"])
def substract():
    global db
    try:
        posted_json = request.get_json()
        print(posted_json)
        addition = posted_json["addition"]
        uuid = addition["uuid"]
        summ = addition["sum"]
    except:
        http_code = 400
        return jsonify({"status":http_code, "result": False}), http_code
    try:
        user = db.select_user_by_uuid(uuid)
        user.substract(summ)
        print(f"sub {summ} from {user.uuid}, now hold is {user.hold}")
        db.update_hold(user)
        return jsonify({"status":200, "result": True, "addition":addition})
    except e.UserNotFoundException:
        http_code = 404
        return jsonify({"status":http_code, "result": False,
                        "addition":{"uuid":uuid},
                        "description": "User is not found in database"}), http_code
    except:
        http_code = 500
        return jsonify({"status":http_code, "result": False}), http_code

@app.route('/api/refresh')
def refresh_db():
    db.drop_table()
    db.create_table()
    return jsonify({"status":200, "result": True})

@app.route('/api/load_db', methods=["POST"])
def load_db_from_json():
    global db
    try:
        posted_json = request.get_json()
        print(posted_json)
        db.load_from_json(posted_json)
        return jsonify({"status":200, "result": True})
    except:
        http_code = 500
        return jsonify({"status":http_code, "result": False}), http_code