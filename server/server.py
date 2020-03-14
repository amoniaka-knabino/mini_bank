import json
from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/ping')
def ping():
    return jsonify({'status':200})

