# user_routes.py
from flask import Blueprint, request, jsonify, make_response, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from app.db_operations import get_db_connection
from app.constants import UserCodes
import hashlib, mysql.connector, secrets, logging

# Create a Blueprint object for user-related routes
user_blueprint = Blueprint("user", __name__)

# Configure logging
logger = logging.getLogger(__name__)

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

# route to register user. Data is passed to another method before any DB write operations are carried out.
@user_blueprint.route("/api/v1/register", methods=['POST'])
def register_user():
    data = request.json
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

# route to log user in and set JWT HTTPOnly cookie
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
                response.set_cookie('access_token_cookie', access_token, httponly=True, path='/')
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

# route to check if user is logged in and also refresh login token
@user_blueprint.route("/api/v1/protected", methods=['GET'])
@jwt_required(optional=True)
def protected():
    current_user = get_jwt_identity()
    if current_user:
        user_id = current_user['user_id']
        fullname = current_user['fullname']
        access_token = create_access_token(identity={'user_id': user_id,'fullname': fullname})
        response = make_response(jsonify({'message': 'Success', 'user': current_user}), 200)
        response.set_cookie('access_token_cookie', access_token, httponly=True, path='/')
        return jsonify({'message': 'Success', 'user': current_user}), 200
    else:
        return jsonify({'message': 'Not logged in'}), 200


# Route for getting or updating user's personal information
@user_blueprint.route("/api/v1/accounts", methods=['GET'])
@jwt_required()
def accounts():
    current_user = get_jwt_identity()
    user_id = current_user['user_id']
    user_details = get_user_details(user_id)
    return user_details

def get_user_details(current_user_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT user_id, user.email, details.fname, details.lname, details.phone, details.address, details.postcode, details.city, details.country, details.registration_datetime
            FROM user
            INNER JOIN details ON user.id = details.user_id
            WHERE user.id = %s
        """, (current_user_id,))
        user_data = cursor.fetchone()
        if user_data:
            user_dict = {
                "user_id": user_data[0],
                "email": user_data[1],
                "fname": user_data[2],
                "lname": user_data[3],
                "phone": user_data[4],
                "address": user_data[5],
                "postcode": user_data[6],
                "city": user_data[7],
                "country": user_data[8],
                "registration_datetime": user_data[9]
            }
            return jsonify(user_dict), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        logger.error("Error fetching user details: %s", e)
        return jsonify({"error": "An unexpected error occurred"}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@user_blueprint.route("/api/v1/moreinfo", methods=['POST'])
def update_user_details():
    data = request.json
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("UPDATE details SET phone = %s, address = %s, postcode = %s, city = %s, country = %s WHERE user_id = %s", (data.get('phoneNumber'), data.get('address'), data.get('postCode'), data.get('city'), data.get('country'), data.get('user_id')))

        connection.commit()

        logger.info("User details updated successfully: %s", data.get('user_id'))
        return jsonify({"message": "User registered successfully", "code": UserCodes.USER_REGISTERED}), 201

    except mysql.connector.Error as err:
        logger.error("Database error during user update: %s", err)
        connection.rollback()
        return jsonify({"error": "Database error"}), 500

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# route to get all product information
@user_blueprint.route('/api/v1/allproducts', methods=['GET'])
def get_all_products():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT sku, fullName, type, SUBSTRING_INDEX(images, ',', 1) AS first_image, star, price, DATE_FORMAT(date, '%Y-%m-%d') AS date FROM product")
        products = cursor.fetchall()
        cursor.close()
        return jsonify(products)
    except Exception as err:
        logger.error("Error fetching all products: %s", err)
        return jsonify({"error": str(err)}), 500
    finally:
        if connection.is_connected():
            cursor.close()

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
    finally:
        if connection.is_connected():
            cursor.close()
    
@user_blueprint.route('/')
def index():
    return render_template('index.html')

@user_blueprint.route('/<string:file_name>')
def render_page(file_name):
    # Assuming your templates are stored in a 'templates' folder
    return render_template(file_name)