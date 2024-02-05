from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask import Blueprint, request, jsonify, make_response
from app.db_operations import get_db_connection
from app.constants import UserCodes
import hashlib, mysql.connector, secrets

user_blueprint = Blueprint("user", __name__)

def prepare_user_data(data):
    required_fields = ['firstname', 'lastname', 'email', 'password']
    
    # Check for the presence of required fields
    if not all(field in data for field in required_fields):
        return None, {"error": "Missing required fields", "code": UserCodes.MISSING_CREDENTIALS}

    # Check for Duplicate Email
    with get_db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT email FROM user WHERE email = %s", (data.get('email'),))
        row = cursor.fetchone()

        if row is not None:
            return None, {"error": "Email is already registered", "code": UserCodes.DUPLICATE_EMAIL}

    # Generate a Random Salt
    salt = secrets.token_hex(32)
    # Combine Client-side Hashed Password with Server-side Salt
    final_hashed_password = hashlib.sha256((data.get('password') + salt).encode('utf-8')).hexdigest()

    return {
        'firstname': data.get('firstname'),
        'lastname': data.get('lastname'),
        'email': data.get('email'),
        'password': final_hashed_password,
        'salt': salt
    }, None

@user_blueprint.route("/api/v1/register", methods=['POST'])
def register_user():
    data = request.json

    # Prepare user data
    user_data, error_response = prepare_user_data(data)

    if error_response:
        return jsonify(error_response), 400

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Insert User into the `user` Table
        cursor.execute("INSERT INTO user (email, password) VALUES (%s, %s)", (user_data['email'], user_data['password']))
        connection.commit()

        # Retrieve the user_id of the inserted user
        cursor.execute("SELECT id FROM user WHERE email = %s", (user_data['email'],))
        user_id = cursor.fetchone()[0]

        # Store the salt in the `userSalt` table
        cursor.execute("INSERT INTO userSalt (user_id, salt) VALUES (%s, %s)", (user_id, user_data['salt']))
        connection.commit()

        # Insert User Details into the `details` Table
        cursor.execute("INSERT INTO details (user_id, fname, lname) VALUES (%s, %s, %s)", (user_id, user_data['firstname'], user_data['lastname']))
        connection.commit()

        return jsonify({"message": "User registered successfully", "code": UserCodes.USER_REGISTERED}), 201

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        connection.rollback()  # Roll back the changes to avoid partial data insertion
        return jsonify({"error": "Database error"}), 500

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@user_blueprint.route("/api/v1/login", methods=['POST'])
def login_user():
    data = request.json
    email = data.get('email')
    hashed_password = data.get('password')  # Hashed password from the frontend

    if not email or not hashed_password:
        return jsonify({"error": "Missing email or password", "code": UserCodes.MISSING_CREDENTIALS}), 400

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Retrieve the user_id, hashed password, and salt from the database
        cursor.execute("SELECT user.id, password, salt FROM user JOIN userSalt ON user.id = userSalt.user_id WHERE email = %s", (email,))
        user_data = cursor.fetchone()
        if user_data:
            user_id, stored_hashed_password, stored_salt = user_data

            # Combine client-side hashed password with the server-side salt and hash again
            entered_password_hash = hashlib.sha256((hashed_password + stored_salt).encode('utf-8')).hexdigest()

            # Compare the hashed passwords
            if entered_password_hash == stored_hashed_password:
                # Create and return a JWT access token
                access_token = create_access_token(identity=user_id)

                # Set the token as a cookie in the response
                response = make_response(jsonify({"message": "Login successful"}), 200)
                response.set_cookie('access_token_cookie', access_token, httponly=True)

                return response
            else:
                return jsonify({"error": "Incorrect username or password", "code": UserCodes.INCORRECT_CREDENTIALS}), 401
        else:
            return jsonify({"error": "Incorrect username or password", "code": UserCodes.INCORRECT_CREDENTIALS}), 401

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return jsonify({"error": "Database error"}), 500

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@user_blueprint.route("/api/v1/protected", methods=['GET'])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@user_blueprint.route("/")
@user_blueprint.route("/index.html")
def home():
    return "Hello world!"