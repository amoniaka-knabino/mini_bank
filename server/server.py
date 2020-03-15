import json
from flask import Flask, jsonify
app = Flask(__name__)

from Database import Database
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

