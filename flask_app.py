from flask import Flask, request, jsonify, render_template
from flask_httpauth import HTTPBasicAuth
import json
import os

app = Flask(__name__)
auth = HTTPBasicAuth()

# Path to the configuration file
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")

# Hardcoded username and password
USERNAME = "admin"  # Replace with your desired username
PASSWORD = "password"  # Replace with your desired password

# Store credentials in a dictionary
USERS = {USERNAME: PASSWORD}


@auth.verify_password
def verify_password(username, password):
    """Verify username and password for basic authentication."""
    if username in USERS and USERS[username] == password:
        return username
    return None


@app.route("/")
@auth.login_required
def index():
    """Render the main configuration page."""
    with open(CONFIG_FILE, "r") as file:
        config = json.load(file)

    # Ensure telegram_bot_token and telegram_chat_id are strings
    config["telegram_bot_token"] = config.get("telegram_bot_token", "")
    config["telegram_chat_id"] = config.get("telegram_chat_id", "")

    return render_template("index.html", config=config)


@app.route("/update", methods=["POST"])
@auth.login_required
def update_config():
    """Update the configuration file with user input."""
    data = request.json
    with open(CONFIG_FILE, "w") as file:
        json.dump(data, file, indent=4)
    return jsonify({"message": "Configuration updated successfully"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
