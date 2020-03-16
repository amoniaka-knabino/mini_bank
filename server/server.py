import json
from flask import Flask, jsonify, request
from Database import Database
import exceptions as e
app = Flask(__name__)
db = None

@app.before_request
def before_request():
    global db 
    db = Database("subscribers.db")
    db.load_from_json("example.json")

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/ping')
def ping():
    return jsonify({'status':200})

@app.route('/api/subs')
def users():
    return jsonify(db.dump_users_to_dict_for_json())

@app.route('/api/status')
def user():
    global db
    try:
        uuid = request.args.get('uuid')
        addition = db.select_user_by_uuid(uuid).dict_for_json()
        return jsonify({"status":200, "result": True, "addition":addition})
    except e.UserNotFoundException:
        http_code = 500
        return jsonify({"status":http_code, "result": False,
                        "addition":{"uuid":uuid}, "description": "User is not found in database"}), http_code
    except:
        http_code = 500
        return jsonify({"status":http_code, "result": False}), http_code