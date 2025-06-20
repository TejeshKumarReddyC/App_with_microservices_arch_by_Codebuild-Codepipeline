import os
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# Load backend service URL (e.g., http://backend.myapp.local:5000)
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend.myapp.local:5000")

@app.route('/')
def index():
    try:
        response = requests.get(f"{BACKEND_URL}/users", timeout=3)
        users = response.json()
        return jsonify(users)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error connecting to backend: {str(e)}"}), 500

@app.route('/add-user', methods=['POST'])
def add_user():
    try:
        data = request.get_json()
        response = requests.post(f"{BACKEND_URL}/users", json=data, timeout=3)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error posting to backend: {str(e)}"}), 500

@app.route('/health')
def health():
    return jsonify({"message": "Frontend is running"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
