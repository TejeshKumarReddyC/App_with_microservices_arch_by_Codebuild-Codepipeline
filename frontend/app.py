import os
import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# ✅ Get backend API URL from environment variable
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:5000")

@app.route('/')
def index():
    try:
        # Call the backend to get user list
        response = requests.get(f"{BACKEND_URL}/users")
        users = response.json()
        return jsonify(users)
    except Exception as e:
        return jsonify({"error": f"Error connecting to backend: {str(e)}"}), 500

@app.route('/add-user', methods=['POST'])
def add_user():
    try:
        data = request.get_json()
        response = requests.post(f"{BACKEND_URL}/users", json=data)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": f"Error posting to backend: {str(e)}"}), 500

@app.route('/health')
def health():
    return jsonify({"message": "Frontend is running"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
