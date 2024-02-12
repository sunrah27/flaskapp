import logging
from logging.handlers import RotatingFileHandler
from flask import Blueprint, request, jsonify, make_response, send_file, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from app.db_operations import get_db_connection
from app.constants import UserCodes
from app.config import DOMAIN
import hashlib
import mysql.connector
import secrets

user_blueprint = Blueprint("user", __name__)

# Configure logging
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

def prepare_user_data(data):
    required_fields = ['firstname', 'lastname', 'email', 'password', 'checkBox']
    
    if (required_fields[4] == 'false'):
        logger.error("Invalid form submission will not procees. %s", UserCodes.FAKE_SUBMISSION)
        return None, {"error": "Invald form submission will not proceed", "code": UserCodes.FAKE_SUBMISSION}

    if not all(field in data for field in required_fields[:4]):  # Slice to include only the first four fields
        logger.error("Missing required fields during user registration. %s", UserCodes.MISSING_CREDENTIALS)
        return None, {"error": "Missing required fields", "code": UserCodes.MISSING_CREDENTIALS}

    with get_db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT email FROM user WHERE email = %s", (data.get('email'),))
        row = cursor.fetchone()

        if row is not None:
            logger.error("Email is already registered during user registration. %s", UserCodes.DUPLICATE_EMAIL)
            return None, {"error": "Email is already registered", "code": UserCodes.DUPLICATE_EMAIL}

    salt = secrets.token_hex(32)
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
    print(data)
    user_data, error_response = prepare_user_data(data)

    if error_response:
        logger.error("API Data error. %s", error_response)
        return jsonify(error_response), 400

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("INSERT INTO user (email, password) VALUES (%s, %s)", (user_data['email'], user_data['password']))
        connection.commit()

        cursor.execute("SELECT id FROM user WHERE email = %s", (user_data['email'],))
        user_id = cursor.fetchone()[0]

        cursor.execute("INSERT INTO userSalt (user_id, salt) VALUES (%s, %s)", (user_id, user_data['salt']))
        connection.commit()

        cursor.execute("INSERT INTO details (user_id, fname, lname) VALUES (%s, %s, %s)", (user_id, user_data['firstname'], user_data['lastname']))
        connection.commit()

        logger.info("User registered successfully: %s", user_data['email'])
        return jsonify({"message": "User registered successfully", "code": UserCodes.USER_REGISTERED}), 201

    except mysql.connector.Error as err:
        logger.error("Database error during user registration: %s", err)
        connection.rollback()
        return jsonify({"error": "Database error"}), 500

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@user_blueprint.route("/api/v1/login", methods=['POST'])
def login_user():
    data = request.json
    email = data.get('email')
    hashed_password = data.get('password')

    if not email or not hashed_password:
        logger.error("Missing email or password during login attempt. %s", UserCodes.MISSING_CREDENTIALS)
        return jsonify({"error": "Missing email or password", "code": UserCodes.MISSING_CREDENTIALS}), 400

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # cursor.execute("SELECT user.id, password, salt FROM user JOIN userSalt ON user.id = userSalt.user_id WHERE email = %s", (email,))
        cursor.execute("SELECT user.id, user.password, userSalt.salt, details.fname, details.lname FROM user JOIN userSalt ON user.id = userSalt.user_id JOIN details ON user.id = details.user_id WHERE user.email = %s", (email,))
        user_data = cursor.fetchone()

        if user_data:
            user_id, stored_hashed_password, stored_salt, fname, lname = user_data
            entered_password_hash = hashlib.sha256((hashed_password + stored_salt).encode('utf-8')).hexdigest()

            if entered_password_hash == stored_hashed_password:
                # Combine fname and lname into Fullname
                fullname = f"{fname} {lname}"
                access_token = create_access_token(identity={'user_id': user_id,'fullname': fullname})
                response = make_response(jsonify({"message": "Login successful"}), 200)
                response.headers.set('Set-Cookie', f'access_token_cookie={access_token}; Domain=sunrah27.github.io/; Secure; HttpOnly; Path=/')
                logger.info("Login successful: %s: %s", user_id, email)
                return response
            else:
                logger.error("Incorrect username or password during login attempt. %s", UserCodes.INCORRECT_CREDENTIALS)
                return jsonify({"error": "Incorrect username or password", "code": UserCodes.INCORRECT_CREDENTIALS}), 401
        else:
            logger.error("Incorrect username or password during login attempt. %s", UserCodes.INCORRECT_CREDENTIALS)
            return jsonify({"error": "Incorrect username or password", "code": UserCodes.INCORRECT_CREDENTIALS}), 401

    except mysql.connector.Error as err:
        logger.error("Database error during login: %s", err)
        return jsonify({"error": "Database error"}), 500

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@user_blueprint.route("/api/v1/protected", methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    logger.info("Protected route accessed by user: %s", current_user)
    return jsonify(logged_in_as=current_user), 200

@user_blueprint.route("/accounts", methods=['GET'])
@jwt_required()
def accounts():
    try:
        current_user_id = get_jwt_identity()
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT user.email, details.fname, details.lname, details.phone, details.address, details.postcode, details.city, details.country, details.registration_datetime FROM user INNER JOIN details ON user.id = details.user_id WHERE user.id = %s", (current_user_id,))
        user_data = cursor.fetchone()

        if user_data:
            return jsonify(user_data)
        else:
            return jsonify({"error": "User not found"}), 404

    except Exception as err:
        logger.error("Error fetching user details: %s", err)
        return jsonify({"error": "An unexpected error occurred"}), 500

    finally:
        cursor.close()
        connection.close()

@user_blueprint.route('/api/v1/allproducts', methods=['GET'])
def get_all_products():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT sku, fullName, type, SUBSTRING_INDEX(images, ',', 1) AS first_image, star, price FROM product")
        products = cursor.fetchall()
        cursor.close()
        return jsonify(products)
    except Exception as err:
        logger.error("Error fetching all products: %s", err)
        return jsonify({"error": str(err)}), 500

@user_blueprint.route('/api/v1/productdetails', methods=['GET'])
def get_product_details():
    try:
        sku = request.args.get('sku')
        if not sku:
            return jsonify({"message": "SKU parameter is required", "code": UserCodes.MISSING_SKU}), 400

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM product WHERE sku = %s", (sku,))
        product = cursor.fetchone()
        cursor.close()

        if product:
            return jsonify(product)
        else:
            return jsonify({"message": "Product not found", "code": UserCodes.PRODUCT_NOT_FOUND}), 404
    except Exception as err:
        logger.error("Error fetching product details: %s", err)
        return jsonify({"error": str(err), "code": UserCodes.DATABASE_CONNECTION_ERROR}), 500

# Default home page. Possible change the page to display log data
@user_blueprint.route("/")
@user_blueprint.route("/index.html")
def home():
    return send_file('index.html')

# Access log file as an API.
@user_blueprint.route("/api/v1/logs", methods=['GET'])
def get_logs():
    try:
        with open('app.log', 'r') as log_file:
            logs = log_file.readlines()
            formatted_logs = ['<p style="background-color: #3a3a3a; color: white; padding: 3px; margin: 0px;">' + format_log(log.strip()) + '</p>' for log in logs]
            return '\n'.join(formatted_logs)
    except Exception as e:
        logger.error("Error accessing log file: %s", e)
        return str(e), 500

def format_log(log):
    parts = log.split(' - ')
    if len(parts) >= 4:
        timestamp, _, level, message = parts[:4]
        if level == 'INFO':
            return f'<span style="color: green;">{timestamp} - {level}</span>: {message}'
        elif level == 'ERROR':
            return f'<span style="color: red;">{timestamp} - {level}</span>: {message}'
        elif level == 'WARNING':
            return f'<span style="color: yellow;">{timestamp} - {level}</span>: {message}'
    return log