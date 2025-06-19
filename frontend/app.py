from flask import Flask, render_template_string
import requests
import os

app = Flask(__name__)

# Backend API URL (internal ECS service DNS or environment variable)
BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:5000")

@app.route("/")
def index():
    try:
        response = requests.get(f"{BACKEND_URL}/")
        users = response.json()
    except Exception as e:
        return f"<h2>Error connecting to backend: {e}</h2>"

    # Render user list in simple HTML
    html = """
    <h1>Users List</h1>
    {% if users %}
        <ul>
        {% for user in users %}
            <li>{{ user.id }} - {{ user.name }}</li>
        {% endfor %}
        </ul>
    {% else %}
        <p>No users found.</p>
    {% endif %}
    """
    return render_template_string(html, users=users)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
