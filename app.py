# app.py

from flask import Flask, request, jsonify
import mysql.connector
from config import db_config
import hashlib
import secrets

app = Flask(__name__)

def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        print("Database connection successful.")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        # Handle the error or just return None
        return None

# Custom codes
user_registered_code = 2010
user_loggedin_code = 2011
missing_credentials_code = 4011
incorrect_credentials_code = 4012
duplicate_email_code = 4013

@app.route("/api/register", methods=['POST'])
def register_user():
    data = request.json

    def validate_registration_data(data):
        required_fields = ['username', 'password', 'email', 'firstname', 'lastname']
        return all(field in data for field in required_fields)

    # Validate registration data
    if not validate_registration_data(data):
        return jsonify({"error": "Missing required fields", "code": missing_credentials_code}), 400

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Check for Duplicate Email (First Check)
        cursor.execute("SELECT user_id FROM details WHERE email = %s", (data.get('email'),))
        if cursor.fetchone():
            return jsonify({"error": "Email is already registered", "code": duplicate_email_code}), 400

        # Generate a Random Salt
        salt = secrets.token_hex(32)

        # Combine Client-side Hashed Password with Server-side Salt
        final_hashed_password = hashlib.sha256((data.get('password') + salt).encode('utf-8')).hexdigest()

        # Insert User into the `user` Table
        cursor.execute("INSERT INTO user (username, password) VALUES (%s, %s)", (data.get('username'), final_hashed_password))
        connection.commit()

        # Retrieve the user_id of the inserted user
        cursor.execute("SELECT id FROM user WHERE username = %s", (data.get('username'),))
        user_id = cursor.fetchone()[0]

        # Store the salt in the `userSalt` table
        cursor.execute("INSERT INTO userSalt (user_id, salt) VALUES (%s, %s)", (user_id, salt))
        connection.commit()

        # Insert User Details into the `details` Table
        cursor.execute("INSERT INTO details (user_id, fname, lname, email) VALUES (%s, %s, %s, %s)",
                       (user_id, data.get('firstname'), data.get('lastname'), data.get('email')))
        connection.commit()

        return jsonify({"message": "User registered successfully", "code": user_registered_code}), 201

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        connection.rollback()  # Roll back the changes to avoid partial data insertion
        return jsonify({"error": "Database error"}), 500

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route("/api/login", methods=['POST'])
def login_user():
    data = request.json
    login_username = data.get('username')
    hashed_password = data.get('password')  # Hashed password from the frontend

    if not login_username or not hashed_password:
        return jsonify({"error": "Missing username or password", "code": missing_credentials_code}), 400

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Retrieve the user_id, hashed password, and salt from the database
        cursor.execute("SELECT user.id, password, salt FROM user JOIN userSalt ON user.id = userSalt.user_id WHERE username = %s", (login_username,))
        user_data = cursor.fetchone()

        if user_data:
            user_id, stored_hashed_password, stored_salt = user_data

            # Combine client-side hashed password with the server-side salt and hash again
            entered_password_hash = hashlib.sha256((hashed_password + stored_salt).encode('utf-8')).hexdigest()

            # Compare the hashed passwords
            if entered_password_hash == stored_hashed_password:
                return jsonify({"message": "Login successful", "code": user_loggedin_code}), 200
            else:
                return jsonify({"error": "Incorrect username or password", "code": incorrect_credentials_code}), 401
        else:
            return jsonify({"error": "Incorrect username or password", "code": incorrect_credentials_code}), 401

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return jsonify({"error": "Database error"}), 500

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route("/")
def home():
    return "Welcome to the Flask app! This is the main page."

if __name__ == "__main__":
    app.run(debug=True)