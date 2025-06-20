from flask import Flask, request, jsonify
import boto3
import mysql.connector
import json
import os

app = Flask(__name__)

# Load DB credentials from Secrets Manager
def get_db_creds():
    secret_name = os.getenv("DB_SECRET_NAME", "myapp_secret")
    region_name = os.getenv("AWS_REGION", "ap-south-1")

    client = boto3.client('secretsmanager', region_name=region_name)
    response = client.get_secret_value(SecretId=secret_name)
    secret = json.loads(response['SecretString'])

    return {
        "host": secret['host'],
        "user": secret['username'],
        "password": secret['password'],
        "database": secret['database'],
        "port": int(secret.get('port', 3306))
    }

# Create DB connection
def get_connection():
    creds = get_db_creds()
    return mysql.connector.connect(
        host=creds['host'],
        user=creds['user'],
        password=creds['password'],
        database=creds['database'],
        port=creds['port']
    )

@app.route('/')
def home():
    return jsonify({"message": "Backend is running!"})

@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({"error": "Name and email required"}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "User added successfully!"})

@app.route('/users', methods=['GET'])
def get_users():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, email FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
